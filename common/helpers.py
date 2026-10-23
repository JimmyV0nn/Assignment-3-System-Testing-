"""Reusable actions shared by every module (login, registration, waits, screenshots)."""
import os
import time
import uuid

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.config import DEFAULT_PASSWORD, DEFAULT_TIMEOUT, SCREENSHOT_DIR, url


# ---------- waits ----------

def wait_visible(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_url_contains(driver, text, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.url_contains(text))


def fill(driver, locator, value):
    """Clear an input and type a new value."""
    field = wait_visible(driver, locator)
    field.clear()
    field.send_keys(value)
    return field


def js_click(driver, element):
    """Click via JavaScript - needed for the theme's hidden custom checkboxes/radios."""
    driver.execute_script("arguments[0].click();", element)


# ---------- evidence ----------

def take_screenshot(driver, name):
    """Save a screenshot to screenshots/<name>_<timestamp>.png for the report."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{name}_{time.strftime('%Y%m%d-%H%M%S')}.png")
    driver.save_screenshot(path)
    return path


# ---------- test data ----------

def unique_email(prefix="tester"):
    """Generate a never-used email so each run gets a clean account."""
    return f"{prefix}.{uuid.uuid4().hex[:10]}@example.com"


# ---------- account actions ----------

def register_new_user(driver, firstname="Test", lastname="User", password=DEFAULT_PASSWORD):
    """Register a brand-new account and return its details. Leaves the user logged in."""
    user = {
        "firstname": firstname,
        "lastname": lastname,
        "email": unique_email(),
        "telephone": "0400000000",
        "password": password,
    }
    submit_registration_form(driver, user)
    wait_url_contains(driver, "account/success")
    return user


def submit_registration_form(driver, user):
    """Fill the registration form with the given details and click Continue, without waiting for the result."""
    driver.get(url("account/register"))
    fill(driver, (By.ID, "input-firstname"), user["firstname"])
    fill(driver, (By.ID, "input-lastname"), user["lastname"])
    fill(driver, (By.ID, "input-email"), user["email"])
    fill(driver, (By.ID, "input-telephone"), user["telephone"])
    fill(driver, (By.ID, "input-password"), user["password"])
    fill(driver, (By.ID, "input-confirm"), user["password"])
    js_click(driver, driver.find_element(By.NAME, "agree"))
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()


def login(driver, email, password):
    """Log in through the login page. Returns True if it reached My Account."""
    driver.get(url("account/login"))
    fill(driver, (By.ID, "input-email"), email)
    fill(driver, (By.ID, "input-password"), password)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']").click()
    try:
        wait_url_contains(driver, "account/account", timeout=8)
        return True
    except Exception:
        return False


def logout(driver):
    driver.get(url("account/logout"))


def get_error_messages(driver, timeout=DEFAULT_TIMEOUT):
    """Return the texts of all red validation messages shown under form fields (waits for the first one)."""
    wait_visible(driver, (By.CSS_SELECTOR, ".text-danger"), timeout)
    return [e.text for e in driver.find_elements(By.CSS_SELECTOR, ".text-danger") if e.text.strip()]


def get_success_alert(driver, timeout=DEFAULT_TIMEOUT):
    """Return the text of the green success alert shown after saving a form."""
    return wait_visible(driver, (By.CSS_SELECTOR, ".alert-success"), timeout).text
