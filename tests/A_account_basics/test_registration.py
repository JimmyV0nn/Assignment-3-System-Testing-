"""
TC-A01  User Registration
Module: A - Account Basics (Tommy)

Scenario 1 - valid details
  Steps: open Register (route=account/register), fill every field with a never-used email, tick Privacy Policy, click Continue
  Expected: redirect to account/success with the heading "Your Account Has Been Created!"
Scenario 2 - email already registered
  Precondition: email E is already registered (registered_user fixture), then logged out
  Steps: submit the registration form again with email E
  Expected: red warning "E-Mail Address is already registered!" and the page stays on account/register
Scenario 3 - password below the minimum length (boundary value)
  Steps: submit the registration form with a 3-character password (the allowed range is 4-20)
  Expected: field error "Password must be between 4 and 20 characters!" and the page stays on account/register
"""
from selenium.webdriver.common.by import By

from common.helpers import (
    logout,
    register_new_user,
    submit_registration_form,
    take_screenshot,
    unique_email,
    wait_visible,
)


def test_s1_register_with_valid_details(driver):
    # Fill and submit the form with a never-used email; the helper waits for the account/success page.
    register_new_user(driver)

    # The success page heading confirms the account was created, not just that the URL changed.
    heading = wait_visible(driver, (By.CSS_SELECTOR, "#content h1"))
    take_screenshot(driver, "TC-A01_S1_account_created")
    assert "Your Account Has Been Created!" in heading.text


def test_s2_register_with_already_registered_email(driver, registered_user):
    # Precondition: the registered_user fixture registered email E; log out so the form can be filled again.
    logout(driver)

    # Submit the registration form a second time with the same email E.
    submit_registration_form(driver, registered_user)

    # The site must refuse the duplicate with a red warning naming the cause.
    alert = wait_visible(driver, (By.CSS_SELECTOR, ".alert-danger"))
    take_screenshot(driver, "TC-A01_S2_duplicate_email_rejected")
    assert "E-Mail Address is already registered!" in alert.text
    # Staying on account/register shows no second account was created.
    assert "account/register" in driver.current_url


def test_s3_register_with_password_below_minimum_length(driver):
    # Boundary value: the password must be 4-20 characters, so 3 characters is just below the minimum.
    user = {
        "firstname": "Test",
        "lastname": "User",
        "email": unique_email(),
        "telephone": "0400000000",
        "password": "abc",
    }
    submit_registration_form(driver, user)

    # The field-level error under the Password input names the allowed length.
    error = wait_visible(driver, (By.CSS_SELECTOR, "#input-password + .text-danger"))
    take_screenshot(driver, "TC-A01_S3_short_password_rejected")
    assert "Password must be between 4 and 20 characters!" in error.text
    # Staying on account/register shows the account was not created.
    assert "account/register" in driver.current_url
