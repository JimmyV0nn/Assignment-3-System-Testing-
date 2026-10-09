"""pytest fixtures shared by every module."""
import pytest
from selenium import webdriver

from common.config import HEADLESS
from common.helpers import register_new_user, take_screenshot


@pytest.fixture
def driver():
    """A fresh Chrome browser for each test. Selenium Manager downloads the driver automatically."""
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)
    yield drv
    drv.quit()


@pytest.fixture
def registered_user(driver):
    """Register a new, unique account (logged in) so tests never share or break each other's data."""
    return register_new_user(driver)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Automatically screenshot the browser when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            take_screenshot(drv, f"FAILED_{item.name}")
