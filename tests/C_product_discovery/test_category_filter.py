    
"""
TC-C02  Product Category Navigation
Module: C - Product Discovery

Scenario 1 - open a category containing products
  Steps: open the Cameras category from the navigation menu.
  Expected: the Cameras heading appears and product cards are displayed.
Scenario 2 - open a nested subcategory
  Steps: hover over Components, then select Monitors.
  Expected: the Monitors heading appears and product cards are displayed.
Scenario 3 - open a category without products
  Steps: open the Software category from the navigation menu.
  Expected: the Software heading appears and no product cards are displayed.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.config import BASE_URL
from common.helpers import take_screenshot, wait_clickable


def open_category(driver, category):
    """Click a main category and wait for its page heading."""
    driver.get(BASE_URL)
    wait_clickable(driver, (By.LINK_TEXT, category)).click()
    return WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#content h2"))
    )


def open_subcategory(driver, category, subcategory):
    """Hover over a main menu item and select its subcategory."""
    driver.get(BASE_URL)
    menu = wait_clickable(driver, (
        By.XPATH, f"//nav[@id='menu']//a[normalize-space()='{category}']"
    ))
    ActionChains(driver).move_to_element(menu).perform()
    link = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((
            By.XPATH,
            f"//nav[@id='menu']//li[contains(@class,'dropdown')]"
            f"[.//a[normalize-space()='{category}']]"
            f"//div[contains(@class,'dropdown-menu')]"
            f"//a[starts-with(normalize-space(), '{subcategory}')]"
        ))
    )
    ActionChains(driver).move_to_element(link).click().perform()
    return WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#content h2"))
    )


def test_s1_open_cameras_category(driver):
    # Open a populated category; verify its heading and product listings.
    heading = open_category(driver, "Cameras")
    products = driver.find_elements(By.CSS_SELECTOR, "#content .product-thumb")

    take_screenshot(driver, "TC-C02_S1_cameras")
    assert heading.text.strip() == "Cameras"
    assert len(products) > 0, "Expected products in Cameras"


def test_s2_open_monitors_subcategory(driver):
    # Navigate through Components > Monitors; verify the destination and products.
    heading = open_subcategory(driver, "Components", "Monitors")
    products = driver.find_elements(By.CSS_SELECTOR, "#content .product-thumb")

    take_screenshot(driver, "TC-C02_S2_monitors")
    assert heading.text.strip() == "Monitors"
    assert len(products) > 0, "Expected products in Monitors"


def test_s3_open_empty_software_category(driver):
    # Open an empty category; verify its heading and absence of product listings.
    heading = open_category(driver, "Software")
    products = driver.find_elements(By.CSS_SELECTOR, "#content .product-thumb")

    take_screenshot(driver, "TC-C02_S3_empty_software")
    assert heading.text.strip() == "Software"
    assert len(products) == 0, "Expected no products in Software"

