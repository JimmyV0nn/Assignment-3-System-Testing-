"""
TC-B02  Change Password
Module: B - Account Management (Jimmy)

Precondition: a registered user is logged in.
Steps:
  1. Open My Account > Password (route=account/password)
  2. Enter a new password in Password and Password Confirm
  3. Click Continue
  4. Log out, then log in with the OLD password
  5. Log in with the NEW password
Expected:
  - Success message "Your password has been successfully updated" is shown
  - Login with the old password is rejected
  - Login with the new password succeeds
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import fill, get_success_alert, login, logout, take_screenshot

NEW_PASSWORD = "NewPass@6789"


def test_change_password(driver, registered_user):
    # Step 1-2: open the page and enter the new password
    driver.get(url("account/password"))
    fill(driver, (By.ID, "input-password"), NEW_PASSWORD)
    fill(driver, (By.ID, "input-confirm"), NEW_PASSWORD)

    # Step 3: save
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B02_success")
    assert "successfully updated" in message

    # Step 4: the old password no longer works
    logout(driver)
    assert not login(driver, registered_user["email"], registered_user["password"]), \
        "Old password should be rejected after changing it"
    take_screenshot(driver, "TC-B02_old_password_rejected")

    # Step 5: the new password works
    assert login(driver, registered_user["email"], NEW_PASSWORD), \
        "New password should allow login"
    take_screenshot(driver, "TC-B02_new_password_login")
