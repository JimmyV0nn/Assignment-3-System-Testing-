"""
TC-B03  Address Book
Module: B - Account Management (Jimmy)

Precondition: a registered user is logged in.

Scenario 1 - Add a new address
  1. Open My Account > Address Book > New Address (route=account/address/add)
  2. Fill in name, address, city, postcode, country (Australia), region (New South Wales)
  3. Click Continue
  Expected: "Your address has been successfully added" and the address appears in the list.

Scenario 2 - Empty required fields are rejected
  1. Open New Address and click Continue without entering anything
  Expected: a validation message under every required field; no address is added.

Scenario 3 - Edit an existing address
  1. Add an address, then click Edit on it in the Address Book
  2. Change the City to "Sydney" and click Continue
  Expected: "Your address has been successfully updated" and the list shows the new city.
"""
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from common.config import DEFAULT_TIMEOUT, url
from common.helpers import fill, get_error_messages, get_success_alert, take_screenshot, wait_visible

ADDRESS = {
    "input-firstname": "Jimmy",
    "input-lastname": "Tester",
    "input-address-1": "15 Broadway",
    "input-city": "Ultimo",
    "input-postcode": "2007",
}
COUNTRY = "Australia"
REGION = "New South Wales"


def _submit(driver):
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()


def _fill_address_form(driver):
    for field_id, value in ADDRESS.items():
        fill(driver, (By.ID, field_id), value)
    Select(driver.find_element(By.ID, "input-country")).select_by_visible_text(COUNTRY)
    _wait_region_loaded(driver, REGION)
    Select(driver.find_element(By.ID, "input-zone")).select_by_visible_text(REGION)


def _wait_region_loaded(driver, region=None):
    """Wait for the AJAX region list to finish loading.

    The site reloads the regions whenever the form opens or the country changes, and disables the
    country list (so it is not submitted) until the load ends.
    """
    def loaded(d):
        options = [o.text for o in Select(d.find_element(By.ID, "input-zone")).options]
        ready = len(options) > 1 if region is None else region in options
        return ready and d.find_element(By.ID, "input-country").is_enabled()

    WebDriverWait(driver, DEFAULT_TIMEOUT, ignored_exceptions=(StaleElementReferenceException,)).until(loaded)


def _add_address(driver):
    driver.get(url("account/address/add"))
    wait_visible(driver, (By.ID, "input-firstname"))
    _wait_region_loaded(driver)
    _fill_address_form(driver)
    _submit(driver)
    return get_success_alert(driver)


def test_add_new_address(driver, registered_user):
    # Step 1: open the New Address form
    driver.get(url("account/address/add"))
    wait_visible(driver, (By.ID, "input-firstname"))
    _wait_region_loaded(driver)

    # Step 2: fill in the form
    _fill_address_form(driver)
    take_screenshot(driver, "TC-B03_S1_form_filled")

    # Step 3: save
    _submit(driver)
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B03_S1_success")
    assert "successfully added" in message

    # The new address is listed in the Address Book
    page = driver.find_element(By.ID, "content").text
    assert ADDRESS["input-address-1"] in page
    assert ADDRESS["input-city"] in page


def test_add_address_required_fields_rejected(driver, registered_user):
    # Step 1: submit the empty form
    driver.get(url("account/address/add"))
    wait_visible(driver, (By.ID, "input-firstname"))
    _wait_region_loaded(driver)
    _submit(driver)

    errors = get_error_messages(driver)
    take_screenshot(driver, "TC-B03_S2_required_fields")
    for expected in (
        "First Name must be between 1 and 32 characters",
        "Last Name must be between 1 and 32 characters",
        "Address must be between 3 and 128 characters",
        "City must be between 2 and 128 characters",
        "Postcode must be between 2 and 10 characters",
        "Please select a region / state",
    ):
        assert any(expected in e for e in errors), f"missing {expected!r} in {errors}"

    # No address was created (the empty list has no rows; its message text varies between sites)
    driver.get(url("account/address"))
    wait_visible(driver, (By.ID, "content"))
    assert not driver.find_elements(By.CSS_SELECTOR, "#content table tr")


def test_edit_address(driver, registered_user):
    # Step 1: add an address, then open it for editing
    _add_address(driver)
    driver.find_element(By.CSS_SELECTOR, "#content a.btn-info").click()
    wait_visible(driver, (By.ID, "input-city"))
    _wait_region_loaded(driver)

    # Step 2: change the city and save
    fill(driver, (By.ID, "input-city"), "Sydney")
    take_screenshot(driver, "TC-B03_S3_form_edited")
    _submit(driver)
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B03_S3_success")
    assert "successfully updated" in message

    page = driver.find_element(By.ID, "content").text
    assert "Sydney" in page
    assert "Ultimo" not in page
