"""
TC-A02  User Login
Module: A - Account Basics (Min Chia Huang)

Precondition (Scenarios 1-2): email E is registered (registered_user fixture), then logged out.
Scenario 1 - valid credentials
  Steps: open Login (route=account/login), enter E and its password, click Login
  Expected: redirect to account/account with the heading "My Account"
Scenario 2 - wrong password
  Steps: enter E and a different password, click Login
  Expected: red warning "No match for E-Mail Address and/or Password." and the page stays on account/login
Scenario 3 - empty fields
  Steps: leave both fields empty, click Login
  Expected: the same no-match warning as Scenario 2 and the page stays on account/login
"""
from selenium.webdriver.common.by import By

from common.helpers import login, logout, take_screenshot, wait_visible

# The site's message for any login it refuses.
NO_MATCH = "No match for E-Mail Address and/or Password."


def test_s1_login_with_valid_credentials(driver, registered_user):
    # Precondition: the registered_user fixture registered email E; log out before testing Login.
    logout(driver)

    # Log in with E and its correct password; login() returns True once account/account loads.
    assert login(driver, registered_user["email"], registered_user["password"]), \
        "Valid credentials should reach My Account"
    # The "My Account" heading confirms the user is logged in, not just that the URL changed.
    heading = wait_visible(driver, (By.CSS_SELECTOR, "#content h2"))
    take_screenshot(driver, "TC-A02_S1_logged_in")
    assert "My Account" in heading.text


def test_s2_login_with_wrong_password(driver, registered_user):
    # Precondition: the registered_user fixture registered email E; log out before testing Login.
    logout(driver)

    # Log in with E and a password that differs from the registered one.
    assert not login(driver, registered_user["email"], "Wrong@9999"), \
        "A wrong password should be rejected"

    # The site must refuse the login with the generic no-match warning.
    alert = wait_visible(driver, (By.CSS_SELECTOR, ".alert-danger"))
    take_screenshot(driver, "TC-A02_S2_wrong_password_rejected")
    assert NO_MATCH in alert.text
    # Staying on account/login shows the user was not logged in.
    assert "account/login" in driver.current_url


def test_s3_login_with_empty_fields(driver):
    # Submit the login form with both fields left empty.
    assert not login(driver, "", ""), "An empty login should be rejected"

    # An empty login is a wrong login, so the site should give the same no-match warning as Scenario 2.
    alert = wait_visible(driver, (By.CSS_SELECTOR, ".alert-danger"))
    take_screenshot(driver, "TC-A02_S3_empty_fields_result")
    assert NO_MATCH in alert.text
    # Staying on account/login shows the user was not logged in.
    assert "account/login" in driver.current_url
