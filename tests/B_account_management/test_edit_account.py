"""
TC-B01  Edit Account Information
Module: B - Account Management (Jimmy)

Precondition: a registered user is logged in.

Scenario 1 - Edit details successfully
  1. Open My Account > Edit Account (route=account/edit)
  2. Change First Name, Last Name and Telephone
  3. Click Continue
  4. Re-open the Edit Account page
  Expected: success message is shown and the form shows the new values.

Scenario 2 - Blank First Name is rejected
  1. Open Edit Account, clear First Name
  2. Click Continue
  Expected: "First Name must be between 1 and 32 characters!" and nothing is saved.

Scenario 3 - Too-short Telephone is rejected
  1. Open Edit Account, set Telephone to "1"
  2. Click Continue
  Expected: "Telephone must be between 3 and 32 characters!" and the old number is kept.
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import fill, get_error_messages, get_success_alert, take_screenshot, wait_visible

NEW_DETAILS = {
    "input-firstname": "Jimmy",
    "input-lastname": "Updated",
    "input-telephone": "0412345678",
}


def _submit(driver):
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()


def test_edit_account_information(driver, registered_user):
    # Step 1: open the Edit Account page
    driver.get(url("account/edit"))
    wait_visible(driver, (By.ID, "input-firstname"))

    # Step 2: change the details
    for field_id, value in NEW_DETAILS.items():
        fill(driver, (By.ID, field_id), value)
    take_screenshot(driver, "TC-B01_S1_form_filled")

    # Step 3: save
    _submit(driver)
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B01_S1_success")
    assert "successfully updated" in message

    # Step 4: values persisted
    driver.get(url("account/edit"))
    for field_id, expected in NEW_DETAILS.items():
        actual = wait_visible(driver, (By.ID, field_id)).get_attribute("value")
        assert actual == expected, f"{field_id}: expected {expected!r}, got {actual!r}"


def test_edit_account_blank_first_name_rejected(driver, registered_user):
    # Step 1: clear First Name
    driver.get(url("account/edit"))
    fill(driver, (By.ID, "input-firstname"), "")

    # Step 2: save
    _submit(driver)
    errors = get_error_messages(driver)
    take_screenshot(driver, "TC-B01_S2_blank_first_name")
    assert any("First Name must be between 1 and 32 characters" in e for e in errors), errors

    # Nothing was saved
    driver.get(url("account/edit"))
    saved = wait_visible(driver, (By.ID, "input-firstname")).get_attribute("value")
    assert saved == registered_user["firstname"]


def test_edit_account_short_telephone_rejected(driver, registered_user):
    # Step 1: enter a too-short telephone number
    driver.get(url("account/edit"))
    fill(driver, (By.ID, "input-telephone"), "1")

    # Step 2: save
    _submit(driver)
    errors = get_error_messages(driver)
    take_screenshot(driver, "TC-B01_S3_short_telephone")
    assert any("Telephone must be between 3 and 32 characters" in e for e in errors), errors

    # The old number is kept
    driver.get(url("account/edit"))
    saved = wait_visible(driver, (By.ID, "input-telephone")).get_attribute("value")
    assert saved == registered_user["telephone"]
