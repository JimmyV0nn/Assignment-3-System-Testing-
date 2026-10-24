"""pytest fixtures, screenshots and result collection for the D module.

One Chrome session per scenario keeps cart, cookies and login state isolated.
Every run writes its own folder under results/ with screenshots, a log and a
summary of the real outcome of all nine scenarios.
"""

from __future__ import annotations

import csv
import json
import platform
import sys
import traceback
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from . import helpers

PROJECT_DIR = Path(__file__).resolve().parent

RUN = {
    "dir": None,
    "started": None,
    "headless": False,
    "env": {},
    "records": {},
}


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False,
                     help="run Chrome without a visible window")
    parser.addoption("--results-dir", action="store", default=str(PROJECT_DIR / "results"),
                     help="root folder that receives one sub-folder per run")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "scenario(id, title): D module scenario id and short English title"
    )
    results_root = Path(config.getoption("--results-dir"))
    run_dir = results_root / datetime.now().strftime("%Y%m%d-%H%M%S")
    (run_dir / "screenshots").mkdir(parents=True, exist_ok=True)

    RUN["dir"] = run_dir
    RUN["started"] = datetime.now().astimezone()
    RUN["headless"] = bool(config.getoption("--headless")) or helpers.headless_requested()
    RUN["env"] = {
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "pytest": pytest.__version__,
        "selenium": _module_version("selenium"),
        "os": platform.platform(),
        "machine": platform.machine(),
        "timezone": str(datetime.now().astimezone().tzinfo),
        "utc_offset": datetime.now().astimezone().strftime("%z"),
    }
    helpers.set_log_path(run_dir / "run.log")
    helpers.note(f"run folder: {run_dir}")
    helpers.note(f"python: {RUN['env']['python']} ({RUN['env']['python_executable']})")
    helpers.note(f"headless: {RUN['headless']}")


def _module_version(name: str) -> str:
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:
        return "unknown"


@pytest.fixture
def driver(request):
    options = Options()
    if RUN["headless"]:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--lang=en-AU")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(90)
    browser.implicitly_wait(0)

    capabilities = browser.capabilities
    RUN["env"]["chrome"] = capabilities.get("browserVersion", "unknown")
    RUN["env"]["chromedriver"] = (
        capabilities.get("chrome", {}).get("chromedriverVersion", "unknown").split(" ")[0]
    )
    helpers.note(f"chrome {RUN['env']['chrome']} / chromedriver {RUN['env']['chromedriver']}")

    yield browser
    try:
        browser.quit()
    except Exception:
        pass


@pytest.fixture
def scenario(request):
    marker = request.node.get_closest_marker("scenario")
    if marker is None:
        pytest.fail("test is missing @pytest.mark.scenario(id, title)")
    return {"id": marker.args[0], "title": marker.args[1] if len(marker.args) > 1 else ""}


@pytest.fixture
def shots(driver, scenario):
    return helpers.Screenshots(driver, RUN["dir"] / "screenshots", scenario["id"])


@pytest.fixture
def account(driver):
    """Register a throw-away account (preparation, not part of the test cases)."""
    try:
        credentials = helpers.register_account(driver)
    except Exception:
        raise helpers.account_failure(traceback.format_exc())
    helpers.note("test account registered (credentials kept in memory only)")
    return credentials


# ---------------------------------------------------------------------------
# Result collection
# ---------------------------------------------------------------------------

def _short_reason(report) -> str:
    text = (report.longreprtext or "").strip()
    if not text:
        return ""
    lines = []
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("E "):
            cleaned = cleaned[2:].strip()
        if cleaned:
            lines.append(cleaned)
    return " | ".join(lines[-3:])[:400]


def _scenario_of(item):
    marker = item.get_closest_marker("scenario")
    if marker is None:
        return item.name, ""
    return marker.args[0], marker.args[1] if len(marker.args) > 1 else ""


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "report_" + report.when, report)

    scenario_id, title = _scenario_of(item)
    record = RUN["records"].setdefault(
        scenario_id,
        {
            "scenario_id": scenario_id,
            "title": title,
            "file": Path(str(item.fspath)).name,
            "test_function": item.name,
            "status": "NOT RUN",
            "duration_seconds": 0.0,
            "reason": "",
        },
    )
    record["duration_seconds"] = round(record["duration_seconds"] + (report.duration or 0), 1)

    if report.when == "setup":
        if report.failed:
            record["status"] = "ERROR"
            record["reason"] = _short_reason(report)
        elif report.skipped:
            record["status"] = "SKIP"
            record["reason"] = _short_reason(report)
    elif report.when == "call":
        if report.failed:
            record["status"] = "FAIL"
            record["reason"] = _short_reason(report)
        elif record["status"] not in ("ERROR", "SKIP"):
            record["status"] = "PASS"
    elif report.when == "teardown" and report.failed and record["status"] == "PASS":
        record["status"] = "ERROR"
        record["reason"] = _short_reason(report)

    if report.failed:
        browser = getattr(item, "funcargs", {}).get("driver")
        if browser is not None:
            path = RUN["dir"] / "screenshots" / f"{scenario_id}_FAILED_{report.when}.png"
            try:
                browser.save_screenshot(str(path))
            except Exception:
                pass


def pytest_sessionfinish(session, exitstatus):
    run_dir = RUN["dir"]
    if run_dir is None:
        return

    records = sorted(RUN["records"].values(), key=lambda record: record["scenario_id"])
    screenshots_dir = run_dir / "screenshots"
    for record in records:
        record["screenshots"] = sorted(
            path.name for path in screenshots_dir.glob(f"{record['scenario_id']}_*.png")
        )

    collected_ids = sorted(
        _scenario_of(item)[0]
        for item in session.items
        if hasattr(item, "get_closest_marker") and item.get_closest_marker("scenario")
    )
    finished = datetime.now().astimezone()
    environment = dict(RUN["env"])
    environment.update(
        {
            "started": RUN["started"].isoformat(timespec="seconds"),
            "finished": finished.isoformat(timespec="seconds"),
            "headless": RUN["headless"],
            "base_url": helpers.BASE,
            "scenarios_collected": len(collected_ids),
        }
    )

    counters = {"PASS": 0, "FAIL": 0, "ERROR": 0, "SKIP": 0, "NOT RUN": 0}
    for record in records:
        counters[record["status"]] = counters.get(record["status"], 0) + 1

    (run_dir / "environment.json").write_text(
        json.dumps(environment, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (run_dir / "summary.json").write_text(
        json.dumps({"environment": environment, "results": records}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (run_dir / "results.csv").open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["scenario_id", "title", "file", "test_function", "status",
                         "duration_seconds", "reason", "screenshots"])
        for record in records:
            writer.writerow([
                record["scenario_id"], record["title"], record["file"],
                record["test_function"], record["status"], record["duration_seconds"],
                record["reason"], "; ".join(record["screenshots"]),
            ])

    lines = [
        "# D Module Test Run Summary",
        "",
        f"- Run folder: `{run_dir.name}`",
        f"- Started: {environment['started']}",
        f"- Finished: {environment['finished']}",
        f"- Time zone: {environment['timezone']} (UTC{environment['utc_offset']})",
        f"- Python: {environment['python']} (`{environment['python_executable']}`)",
        f"- pytest: {environment['pytest']} | Selenium: {environment['selenium']}",
        f"- Chrome: {environment.get('chrome', 'not started')} | chromedriver: {environment.get('chromedriver', 'not started')}",
        f"- OS: {environment['os']} ({environment['machine']})",
        f"- Headless: {environment['headless']}",
        f"- Tested site: {environment['base_url']}",
        f"- Scenarios collected: {len(collected_ids)} (expected 9)",
        f"- Result: PASS {counters['PASS']} / FAIL {counters['FAIL']} / "
        f"ERROR {counters['ERROR']} / SKIP {counters['SKIP']}",
        "",
        "| Scenario | Title | File | Status | Duration (s) | Evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        evidence = ", ".join(record["screenshots"]) or "-"
        reason = f"<br>{record['reason']}" if record["reason"] else ""
        lines.append(
            f"| {record['scenario_id']} | {record['title']} | {record['file']} | "
            f"**{record['status']}**{reason} | {record['duration_seconds']} | {evidence} |"
        )
    lines.append("")
    lines.append("Screenshots and logs for this run are stored in the same folder.")
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    helpers.note("--- run finished ---")
    for record in records:
        helpers.note(f"{record['scenario_id']}: {record['status']} ({record['duration_seconds']}s)")
        if record["reason"]:
            helpers.note(f"    reason: {record['reason']}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if RUN["dir"] is not None:
        terminalreporter.write_sep("-", f"D module results: {RUN['dir']}")
