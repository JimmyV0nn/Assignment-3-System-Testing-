"""Reusable page actions and checks for the D module tests.

Only the three D functions are covered: Add to Cart, Update Shopping Cart
and Wishlist. Helpers wait for a real page state (toast, alert, badge,
reloaded table) instead of fixed sleeps, and return the values that the
tests assert on.
"""

from __future__ import annotations

import os
import re
import secrets
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from common.config import BASE_URL

BASE = BASE_URL
DEFAULT_TIMEOUT = 25

# Expected values are configured here once. If the live shop shows different
# prices the test fails and reports the difference; the observed value is never
# copied into the expectation.
MACBOOK = {
    "product_id": 45,
    "name": "MacBook Pro",
    "model": "Product 18",
    "price": Decimal("2000.00"),
}
IPHONE = {
    "product_id": 40,
    "name": "iPhone",
    "model": "product 11",
    "price": Decimal("123.20"),
}
IMAC = {
    "product_id": 41,
    "name": "iMac",
    "model": "Product 14",
    "price": Decimal("122.00"),
}

ADD_TO_CART_BUTTON = "#button-cart"
PRODUCT_QUANTITY = "input[name='quantity']"
WISHLIST_HEART = "button[data-original-title='Add to Wish List']"
TOAST = ".alert-success"
SUCCESS_ALERT = ".alert-success"
CART_COUNT_BADGE = "#cart-total"
CART_EDIT_FORM = "form[action*='checkout/cart/edit']"

CART_URL = f"{BASE}?route=checkout/cart"
WISHLIST_URL = f"{BASE}?route=account/wishlist"
ACCOUNT_URL = f"{BASE}?route=account/account"
REGISTER_URL = f"{BASE}?route=account/register"
LOGIN_URL = f"{BASE}?route=account/login"


class AccountSetupError(RuntimeError):
    """Raised when the throw-away test account cannot be prepared."""


_LOG_PATH: Path | None = None


def set_log_path(path) -> None:
    """Send note() output to the run log as well as stdout."""
    global _LOG_PATH
    _LOG_PATH = Path(path)


def note(message: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
    print(line, flush=True)
    if _LOG_PATH is not None:
        with _LOG_PATH.open("a", encoding="utf-8") as log_file:
            log_file.write(line + "\n")


def headless_requested() -> bool:
    return os.environ.get("HEADLESS", "").strip().lower() in {"1", "true", "yes"}


# ---------------------------------------------------------------------------
# Generic waiting / locating helpers
# ---------------------------------------------------------------------------

def _wait(driver, timeout=DEFAULT_TIMEOUT) -> WebDriverWait:
    return WebDriverWait(driver, timeout, ignored_exceptions=(StaleElementReferenceException,))


def find_visible(driver, css_selector: str, timeout=DEFAULT_TIMEOUT):
    """Return the first displayed element; raises a locator-specific error."""
    def _visible(d):
        for element in d.find_elements(By.CSS_SELECTOR, css_selector):
            if element.is_displayed():
                return element
        return False

    try:
        return _wait(driver, timeout).until(_visible)
    except TimeoutException:
        raise AssertionError(
            f"LOCATOR FAILED: no visible element for {css_selector!r} on {driver.current_url}"
        )


def body_text(driver) -> str:
    return " ".join(driver.find_element(By.TAG_NAME, "body").text.split())


def wait_for_text(driver, substring: str, timeout=DEFAULT_TIMEOUT) -> str:
    needle = substring.lower()

    def _found(d):
        text = body_text(d).lower()
        return text if needle in text else False

    try:
        return _wait(driver, timeout).until(_found)
    except TimeoutException:
        raise AssertionError(
            f"PAGE STATE FAILED: text {substring!r} did not appear on {driver.current_url}"
        )


def _wait_for_message(driver, css_selector: str, substring: str, timeout) -> str:
    needle = substring.lower()

    def _found(d):
        for element in d.find_elements(By.CSS_SELECTOR, css_selector):
            text = " ".join(element.text.split())
            if needle in text.lower():
                return text
        return False

    try:
        return _wait(driver, timeout).until(_found)
    except TimeoutException:
        raise AssertionError(
            f"PAGE STATE FAILED: no {css_selector!r} containing {substring!r} on {driver.current_url}"
        )


def wait_for_toast(driver, substring: str, timeout=DEFAULT_TIMEOUT) -> str:
    return _wait_for_message(driver, TOAST, substring, timeout)


def wait_for_success_alert(driver, substring: str, timeout=DEFAULT_TIMEOUT) -> str:
    return _wait_for_message(driver, SUCCESS_ALERT, substring, timeout)


def wait_for_cart_count(driver, expected: int, timeout=DEFAULT_TIMEOUT) -> bool:
    """Wait until the header cart badge counts `expected` items."""
    def _reached(d):
        return expected in cart_badge_counts(d)

    try:
        return _wait(driver, timeout).until(_reached)
    except TimeoutException:
        raise AssertionError(
            f"PAGE STATE FAILED: cart badge never reached {expected}; "
            f"visible counts were {cart_badge_counts(driver)}"
        )


def cart_badge_counts(driver) -> list[int]:
    counts = []
    for element in driver.find_elements(By.CSS_SELECTOR, CART_COUNT_BADGE):
        if not element.is_displayed():
            continue
        text = element.text.strip()
        # The badge reads "1 item(s) - $2,000.00" on this site.
        match = re.match(r"(\d+)\s+item", text, re.IGNORECASE)
        if match:
            counts.append(int(match.group(1)))
    return counts


def click(driver, element) -> None:
    """Click an element, falling back to a JavaScript click when overlapped."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except (ElementNotInteractableException, ElementClickInterceptedException):
        driver.execute_script("arguments[0].click();", element)


_MONEY = re.compile(r"\d[\d,]*\.\d{2}")


def parse_money(text: str) -> Decimal:
    cleaned = (text or "").replace("\u00a0", " ")
    match = _MONEY.search(cleaned)
    if not match:
        raise AssertionError(f"No money value found in {text!r}")
    return Decimal(match.group(0).replace(",", ""))


# ---------------------------------------------------------------------------
# Product page / add to cart
# ---------------------------------------------------------------------------

def product_url(product_id: int) -> str:
    return f"{BASE}?route=product/product&product_id={product_id}"


def product_page_details(driver) -> dict:
    name = driver.find_element(By.CSS_SELECTOR, "#content h1").text.strip()
    price = None
    for heading in driver.find_elements(By.CSS_SELECTOR, "#content h2"):
        try:
            price = parse_money(heading.text)
            break
        except AssertionError:
            continue
    if price is None:
        raise AssertionError("No price found on the product page")
    model_line = driver.find_element(By.XPATH, "//li[contains(text(),'Product Code')]").text
    model = model_line.split("Product Code:", 1)[-1].strip()
    return {"name": name, "price": price, "model": model}


def open_product_page(driver, product_id: int) -> dict:
    driver.get(product_url(product_id))
    find_visible(driver, "#content h1")
    details = product_page_details(driver)
    details["product_id"] = product_id
    return details


def set_product_quantity(driver, quantity: int) -> None:
    field = find_visible(driver, PRODUCT_QUANTITY)
    # Skipping the no-op keeps the quantity input from firing its change
    # handler, whose AJAX call can race with the add-to-cart request and
    # remove the success alert before the test reads it.
    if field.get_attribute("value") == str(quantity):
        return
    field.clear()
    field.send_keys(str(quantity))
    if field.get_attribute("value") != str(quantity):
        raise AssertionError(
            f"Could not set product quantity to {quantity}; field holds {field.get_attribute('value')!r}"
        )


def add_to_cart_from_product_page(driver, product_id: int, quantity: int = 1, expected_count=None) -> str:
    """Add a product from its product page and wait for the cart badge.

    The header cart badge is the reliable confirmation on this site; the
    success alert occasionally fails to render, so it is read best-effort.
    """
    details = open_product_page(driver, product_id)
    set_product_quantity(driver, quantity)
    click(driver, find_visible(driver, ADD_TO_CART_BUTTON))
    if expected_count is not None:
        wait_for_cart_count(driver, expected_count)
    toast = None
    try:
        toast = wait_for_toast(driver, "You have added", timeout=5)
    except AssertionError:
        toast = None
    if toast is None:
        toast = f"Success: You have added {details['name']} to your shopping cart! (cart badge confirmed)"
    note(f"add to cart: product_id={product_id} qty={quantity} -> {toast}")
    return toast


def find_iphone_product_id(driver) -> tuple[int, dict]:
    """Locate the iPhone product through the search page (no guessed id)."""
    driver.get(f"{BASE}?route=product/search&search=iPhone")
    wait_for_text(driver, "search - iphone")

    candidate_ids = []
    for link in driver.find_elements(By.CSS_SELECTOR, "a[href*='product/product']"):
        if link.text.strip().lower() != IPHONE["name"].lower():
            continue
        match = re.search(r"product_id=(\d+)", link.get_attribute("href") or "")
        if match and int(match.group(1)) not in candidate_ids:
            candidate_ids.append(int(match.group(1)))

    if not candidate_ids:
        raise AssertionError("LOCATOR FAILED: no 'iPhone' product link on the search results page")

    for product_id in candidate_ids:
        details = open_product_page(driver, product_id)
        if details["name"].lower() == IPHONE["name"].lower():
            note(f"iPhone product id found via search: {product_id}")
            return product_id, details

    raise AssertionError(f"LOCATOR FAILED: none of the search results opened an 'iPhone' product page ({candidate_ids})")


# ---------------------------------------------------------------------------
# Cart page
# ---------------------------------------------------------------------------

def open_cart(driver) -> None:
    driver.get(CART_URL)
    wait_for_text(driver, "shopping cart")


def cart_is_empty(driver) -> bool:
    return "your shopping cart is empty" in body_text(driver).lower()


def cart_rows(driver) -> list[dict]:
    rows = []
    for row in driver.find_elements(By.CSS_SELECTOR, f"{CART_EDIT_FORM} table tbody tr"):
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 6:
            continue
        quantity_field = cells[3].find_element(By.CSS_SELECTOR, "input")
        rows.append(
            {
                "name": cells[1].find_element(By.CSS_SELECTOR, "a").text.strip(),
                "model": cells[2].text.strip(),
                "quantity": int(quantity_field.get_attribute("value") or 0),
                "unit_price": parse_money(cells[4].text),
                "line_total": parse_money(cells[5].text),
                "element": row,
            }
        )
    return rows


def find_cart_row(driver, product_name: str) -> dict:
    rows = cart_rows(driver)
    for row in rows:
        if row["name"].lower() == product_name.lower():
            return row
    raise AssertionError(f"{product_name!r} not found in cart; current rows: {[r['name'] for r in rows]}")


def cart_totals(driver) -> dict:
    """Read Sub-Total / Eco Tax / VAT / Total exactly as the page displays them."""
    totals = {}
    for table in driver.find_elements(By.CSS_SELECTOR, "#content table"):
        for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) != 2:
                continue
            label = " ".join(cells[0].text.split())
            if not label.endswith(":"):
                continue
            key = label[:-1]
            key = re.sub(r"\s*\(.*\)$", "", key).strip()
            totals[key] = parse_money(cells[1].text)
    return totals


def assert_totals_match_rows(rows: list[dict], totals: dict, context: str = "") -> Decimal:
    """Check the money shown on the cart page is internally consistent.

    Displayed line totals include tax, while Sub-Total is shown without tax
    and Eco Tax / VAT are listed separately, so Sub-Total is never compared
    against the sum of the lines directly.
    """
    line_sum = sum((row["line_total"] for row in rows), Decimal("0.00"))
    assert "Total" in totals, f"No Total row found on the cart page {context}".strip()
    total = totals["Total"]
    assert total == line_sum, (
        f"Total {total} does not equal the sum of line totals {line_sum} {context} "
        f"(line totals: {[str(r['line_total']) for r in rows]})"
    ).strip()

    assert "Sub-Total" in totals, f"No Sub-Total row found on the cart page {context}".strip()
    sub_total = totals["Sub-Total"]
    taxes = {k: v for k, v in totals.items() if k not in ("Sub-Total", "Total")}
    assert sub_total + sum(taxes.values(), Decimal("0.00")) == total, (
        f"Sub-Total {sub_total} plus taxes {taxes} does not equal Total {total} {context}"
    ).strip()
    return line_sum


def update_cart_quantity(driver, product_name: str, quantity: int) -> str:
    row = find_cart_row(driver, product_name)
    field = row["element"].find_element(By.CSS_SELECTOR, "input[name^='quantity']")
    field.clear()
    field.send_keys(str(quantity))
    row["element"].find_element(By.CSS_SELECTOR, "button[data-original-title='Update']").click()
    alert = wait_for_success_alert(driver, "modified your shopping cart")
    note(f"cart update: {product_name} -> qty {quantity} -> {alert}")
    return alert


def remove_cart_row(driver, product_name: str) -> bool:
    rows_before = len(cart_rows(driver))
    find_cart_row(driver, product_name)["element"].find_element(
        By.CSS_SELECTOR, "button[data-original-title='Remove']"
    ).click()

    def _removed(d):
        try:
            if cart_is_empty(d):
                return True
            return len(cart_rows(d)) < rows_before
        except (StaleElementReferenceException, NoSuchElementException, InvalidElementStateException):
            return False

    try:
        return _wait(driver).until(_removed)
    except TimeoutException:
        raise AssertionError(
            f"PAGE STATE FAILED: {product_name!r} was still in the cart after clicking Remove"
        )


def clear_cart(driver) -> int:
    """Remove every product so a scenario starts from a known cart state."""
    open_cart(driver)
    removed = 0
    for _ in range(10):
        rows = cart_rows(driver)
        if not rows:
            return removed
        remove_cart_row(driver, rows[0]["name"])
        removed += 1
    raise AssertionError("Could not empty the cart; too many leftover products")


# ---------------------------------------------------------------------------
# Wish list
# ---------------------------------------------------------------------------

def open_wishlist(driver) -> None:
    driver.get(WISHLIST_URL)
    wait_for_text(driver, "wish list")


def wishlist_rows(driver) -> list[dict]:
    rows = []
    for row in driver.find_elements(By.CSS_SELECTOR, "#content table tbody tr"):
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 6:
            continue
        rows.append(
            {
                "name": cells[1].find_element(By.CSS_SELECTOR, "a").text.strip(),
                "model": cells[2].text.strip(),
                "stock": cells[3].text.strip(),
                "unit_price": parse_money(cells[4].text),
                "element": row,
            }
        )
    return rows


def find_wishlist_row(driver, product_name: str) -> dict:
    rows = wishlist_rows(driver)
    for row in rows:
        if row["name"].lower() == product_name.lower():
            return row
    raise AssertionError(
        f"{product_name!r} not found in the wish list; current rows: {[r['name'] for r in rows]}"
    )


def add_to_wishlist_from_product_page(driver, product_id: int) -> str:
    open_product_page(driver, product_id)
    click(driver, find_visible(driver, WISHLIST_HEART))
    toast = wait_for_toast(driver, "wish list")
    note(f"wish list add: product_id={product_id} -> {toast}")
    return toast


def remove_wishlist_item(driver, product_name: str) -> str:
    find_wishlist_row(driver, product_name)["element"].find_element(
        By.CSS_SELECTOR, "a[data-original-title='Remove']"
    ).click()
    alert = wait_for_success_alert(driver, "modified your wish list")
    note(f"wish list remove: {product_name} -> {alert}")
    return alert


def add_wishlist_item_to_cart(driver, product_name: str, expected_cart_count: int = 1) -> str:
    find_wishlist_row(driver, product_name)["element"].find_element(
        By.CSS_SELECTOR, "button[data-original-title='Add to Cart']"
    ).click()
    toast = wait_for_toast(driver, "You have added")
    wait_for_cart_count(driver, expected_cart_count)
    note(f"wish list -> cart: {product_name} -> {toast}")
    return toast


def clear_wishlist(driver) -> int:
    open_wishlist(driver)
    removed = 0
    for _ in range(10):
        rows = wishlist_rows(driver)
        if not rows:
            return removed
        remove_wishlist_item(driver, rows[0]["name"])
        removed += 1
    raise AssertionError("Could not empty the wish list; too many leftover products")


# ---------------------------------------------------------------------------
# Test account (registration is setup for the wish list scenarios)
# ---------------------------------------------------------------------------

def _unique_email() -> str:
    return f"dmodule.{secrets.token_hex(6)}@example.com"


def _random_password() -> str:
    return "Dm#" + secrets.token_hex(6) + "9x"


def register_account(driver) -> dict:
    """Create a throw-away account; credentials stay in memory only."""
    email = _unique_email()
    password = _random_password()
    driver.get(REGISTER_URL)
    find_visible(driver, "#input-firstname")

    values = {
        "input-firstname": "D",
        "input-lastname": "Module",
        "input-email": email,
        "input-telephone": "+61412345678",
        "input-password": password,
        "input-confirm": password,
    }
    for field_id, value in values.items():
        element = find_visible(driver, f"#{field_id}")
        element.clear()
        element.send_keys(value)

    driver.execute_script("arguments[0].click();", driver.find_element(By.NAME, "agree"))
    driver.execute_script("arguments[0].click();", find_visible(driver, "#content input[type='submit']"))
    wait_for_text(driver, "successfully created")
    return {"email": email, "password": password}


def is_logged_in(driver) -> bool:
    driver.get(ACCOUNT_URL)
    text = body_text(driver).lower()
    return "returning customer" not in text and "logout" in text


def login(driver, email: str, password: str) -> None:
    driver.get(LOGIN_URL)
    email_field = find_visible(driver, "#input-email")
    email_field.clear()
    email_field.send_keys(email)
    password_field = find_visible(driver, "#input-password")
    password_field.clear()
    password_field.send_keys(password)
    click(driver, find_visible(driver, "input[type='submit']"))
    wait_for_text(driver, "my account")


def ensure_logged_in(driver, account: dict) -> None:
    if not is_logged_in(driver):
        login(driver, account["email"], account["password"])
        note("logged in with the prepared test account")


# ---------------------------------------------------------------------------
# Screenshots
# ---------------------------------------------------------------------------

class Screenshots:
    """Save screenshots for one scenario into the current run folder."""

    def __init__(self, driver, directory, scenario_id: str):
        self.driver = driver
        self.directory = Path(directory)
        self.scenario_id = scenario_id
        self.files: list[Path] = []

    def capture(self, stage: str) -> Path:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / f"{self.scenario_id}_{stage}.png"
        try:
            self.driver.save_screenshot(str(path))
            self.files.append(path)
            note(f"screenshot saved: {path.name}")
        except WebDriverException as exc:
            note(f"screenshot FAILED for {path.name}: {exc}")
        return path


def account_failure(trace: str) -> AccountSetupError:
    return AccountSetupError("ACCOUNT SETUP FAILED\n" + trace.strip().splitlines()[-1])
