"""
TC-B03  Add a New Address to the Address Book
Module: B - Account Management (Jimmy)

Precondition: a registered user is logged in.
Steps:
  1. Open My Account > Address Book > New Address (route=account/address/add)
  2. Fill in name, address, city, postcode, country (Australia), region (New South Wales)
  3. Click Continue
Expected:
  - Success message "Your address has been successfully added" is shown
  - The new address appears in the Address Book list
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from common.config import DEFAULT_TIMEOUT, url
from common.helpers import fill, get_success_alert, take_screenshot, wait_visible

ADDRESS = {
    "input-firstname": "Jimmy",
    "input-lastname": "Tester",
    "input-address-1": "15 Broadway",
    "input-city": "Ultimo",
    "input-postcode": "2007",
}
COUNTRY = "Australia"
REGION = "New South Wales"


def test_add_new_address(driver, registered_user):
    # Step 1: open the New Address form
    driver.get(url("account/address/add"))
    wait_visible(driver, (By.ID, "input-firstname"))

    # Step 2: fill in the form
    for field_id, value in ADDRESS.items():
        fill(driver, (By.ID, field_id), value)
    Select(driver.find_element(By.ID, "input-country")).select_by_visible_text(COUNTRY)
    # The region list reloads by AJAX after choosing a country
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        lambda d: REGION in [o.text for o in Select(d.find_element(By.ID, "input-zone")).options]
    )
    Select(driver.find_element(By.ID, "input-zone")).select_by_visible_text(REGION)
    take_screenshot(driver, "TC-B03_form_filled")

    # Step 3: save
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()
    message = get_success_alert(driver)
    take_screenshot(driver, "TC-B03_success")
    assert "successfully added" in message

    # The new address is listed in the Address Book
    page = driver.find_element(By.ID, "content").text
    assert ADDRESS["input-address-1"] in page
    assert ADDRESS["input-city"] in page
