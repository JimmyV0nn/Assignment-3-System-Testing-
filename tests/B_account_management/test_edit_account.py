"""
TC-B01  Edit Account Information
Module: B - Account Management (Jimmy)

Precondition: a registered user is logged in.
Steps:
  1. Open My Account > Edit Account (route=account/edit)
  2. Change First Name, Last Name and Telephone
  3. Click Continue
  4. Re-open the Edit Account page
Expected:
  - Success message "Your account has been successfully updated" is shown
  - The edit form shows the new values (changes were saved)
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import fill, get_success_alert, take_screenshot, wait_visible

NEW_DETAILS = {
    "input-firstname": "Jimmy",
    "input-lastname": "Updated",
    "input-telephone": "0412345678",
}


def test_edit_account_information(driver, registered_user):
    # Step 1: open the Edit Account page
    driver.get(url("account/edit"))
    wait_visible(driver, (By.ID, "input-firstname"))

    # Step 2: change the details
    for field_id, value in NEW_DETAILS.items():
        fill(driver, (By.ID, field_id), value)
    take_screenshot(driver, "TC-B01_form_filled")

    # Step 3: save
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B01_success")
    assert "successfully updated" in message

    # Step 4: values persisted
    driver.get(url("account/edit"))
    for field_id, expected in NEW_DETAILS.items():
        actual = wait_visible(driver, (By.ID, field_id)).get_attribute("value")
        assert actual == expected, f"{field_id}: expected {expected!r}, got {actual!r}"
