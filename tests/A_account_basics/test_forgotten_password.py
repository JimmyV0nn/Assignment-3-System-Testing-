"""
TC-A03  Forgotten Password
Module: A - Account Basics (Tommy)

Scenario 1 - registered email
  Precondition: email E is registered (registered_user fixture), then logged out
  Steps: open Forgotten Password (route=account/forgotten), enter E, click Continue
  Expected: redirect to account/login with a green message "An email with a confirmation link has been sent..."
Scenario 2 - unregistered email
  Steps: enter a never-registered email, click Continue
  Expected: red warning "The E-Mail Address was not found in our records, please try again!" and the page stays on account/forgotten
Scenario 3 - empty email
  Steps: leave the email field empty, click Continue
  Expected: a red warning, no green success message, and the page stays on account/forgotten
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import fill, logout, take_screenshot, unique_email, wait_url_contains, wait_visible

# The site's warning for an email address it has no account for.
NOT_FOUND = "The E-Mail Address was not found in our records, please try again!"


def request_password_reset(driver, email):
    # Open the forgotten password form, enter the email and click Continue.
    driver.get(url("account/forgotten"))
    fill(driver, (By.ID, "input-email"), email)
    driver.find_element(By.CSS_SELECTOR, "#content input[type='submit']").click()


def test_s1_reset_with_registered_email(driver, registered_user):
    # Precondition: the registered_user fixture registered email E; log out before requesting a reset.
    logout(driver)

    # Request a reset link for E on the forgotten password form.
    request_password_reset(driver, registered_user["email"])

    # An accepted request redirects to the login page.
    wait_url_contains(driver, "account/login")
    # Check only the opening phrase of the success message, so a fix to defect D1's wording still passes.
    alert = wait_visible(driver, (By.CSS_SELECTOR, ".alert-success"))
    take_screenshot(driver, "TC-A03_S1_reset_email_sent")
    assert "An email with a confirmation link has been sent" in alert.text


def test_s2_reset_with_unregistered_email(driver):
    # Request a reset link for a fresh email that has never been registered.
    request_password_reset(driver, unique_email())

    # The site must refuse the request with a warning that the email is unknown.
    alert = wait_visible(driver, (By.CSS_SELECTOR, ".alert-danger"))
    take_screenshot(driver, "TC-A03_S2_unknown_email_rejected")
    assert NOT_FOUND in alert.text
    # Staying on account/forgotten shows no reset email was sent.
    assert "account/forgotten" in driver.current_url


def test_s3_reset_with_empty_email(driver):
    # Submit the forgotten password form with the email field left empty.
    request_password_reset(driver, "")

    # Requirement: the site must refuse an empty address with a red warning.
    wait_visible(driver, (By.CSS_SELECTOR, ".alert-danger"))
    take_screenshot(driver, "TC-A03_S3_empty_email_rejected")
    # No green success message may appear, because no reset email can be sent to an empty address.
    assert not driver.find_elements(By.CSS_SELECTOR, ".alert-success")
    # Staying on account/forgotten shows the request was not accepted.
    assert "account/forgotten" in driver.current_url
