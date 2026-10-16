"""
TC-B02  Change Password
Module: B - Account Management (Jimmy)

Precondition: a registered user is logged in.

Scenario 1 - Change password successfully
  1. Open My Account > Password (route=account/password)
  2. Enter a new password in Password and Password Confirm
  3. Click Continue
  4. Log out, then log in with the OLD password
  5. Log in with the NEW password
  Expected: success message; old password rejected; new password accepted.

Scenario 2 - Mismatched confirmation is rejected
  1. Open the Password page, enter a new password and a different confirmation
  2. Click Continue
  Expected: "Password confirmation does not match password!" and the old password still works.

Scenario 3 - Too-short password is rejected
  1. Open the Password page, enter "ab" in both fields
  2. Click Continue
  Expected: "Password must be between 4 and 20 characters!" and the old password still works.
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import fill, get_error_messages, get_success_alert, login, logout, take_screenshot

NEW_PASSWORD = "NewPass@6789"


def _submit(driver):
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()


def _try_change_password(driver, password, confirm):
    driver.get(url("account/password"))
    fill(driver, (By.ID, "input-password"), password)
    fill(driver, (By.ID, "input-confirm"), confirm)
    _submit(driver)


def test_change_password(driver, registered_user):
    # Step 1-3: open the page, enter the new password and save
    _try_change_password(driver, NEW_PASSWORD, NEW_PASSWORD)
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B02_S1_success")
    assert "successfully updated" in message

    # Step 4: the old password no longer works
    logout(driver)
    assert not login(driver, registered_user["email"], registered_user["password"]), \
        "Old password should be rejected after changing it"
    take_screenshot(driver, "TC-B02_S1_old_password_rejected")

    # Step 5: the new password works
    assert login(driver, registered_user["email"], NEW_PASSWORD), \
        "New password should allow login"
    take_screenshot(driver, "TC-B02_S1_new_password_login")


def test_change_password_mismatch_rejected(driver, registered_user):
    _try_change_password(driver, NEW_PASSWORD, "Different@1234")
    errors = get_error_messages(driver)
    take_screenshot(driver, "TC-B02_S2_mismatch")
    assert any("Password confirmation does not match password" in e for e in errors), errors

    # The password was not changed
    logout(driver)
    assert login(driver, registered_user["email"], registered_user["password"]), \
        "Old password should still work after a rejected change"


def test_change_password_too_short_rejected(driver, registered_user):
    _try_change_password(driver, "ab", "ab")
    errors = get_error_messages(driver)
    take_screenshot(driver, "TC-B02_S3_too_short")
    assert any("Password must be between 4 and 20 characters" in e for e in errors), errors

    # The password was not changed
    logout(driver)
    assert login(driver, registered_user["email"], registered_user["password"]), \
        "Old password should still work after a rejected change"
