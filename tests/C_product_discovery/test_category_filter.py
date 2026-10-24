
"""
TC-C02: Product Category Navigation
Module: C - Product Discovery
Scenarios: S01, S02, S03
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.config import BASE_URL
from common.helpers import take_screenshot, wait_clickable


def wait_for_heading(driver, category):
    """Wait until the correct category heading is displayed."""
    return WebDriverWait(driver, 15).until(
        lambda d: next(
            (
                h for h in d.find_elements(By.CSS_SELECTOR, "#content h1, #content h2")
                if h.is_displayed() and h.text.strip() == category
            ),
            False
        )
    )


def open_category(driver, category):
    """Click a main category."""
    wait_clickable(driver, (By.LINK_TEXT, category)).click()
    return wait_for_heading(driver, category)


def open_subcategory(driver, category, subcategory):
    """Hover over a main category and click its subcategory."""
    menu = wait_clickable(
        driver,
        (By.XPATH, f"//nav[@id='menu']//a[normalize-space()='{category}']")
    )
    ActionChains(driver).move_to_element(menu).perform()

    link = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                f"//nav[@id='menu']//li[contains(@class,'dropdown')]"
                f"[.//a[normalize-space()='{category}']]"
                f"//div[contains(@class,'dropdown-menu')]"
                f"//a[starts-with(normalize-space(), '{subcategory}')]"
            )
        )
    )

    ActionChains(driver).move_to_element(link).click().perform()
    return wait_for_heading(driver, subcategory)


def test_s1_open_cameras_category(driver):
    """S01: Open Cameras category with products."""
    driver.get(BASE_URL)

    heading = open_category(driver, "Cameras")
    products = driver.find_elements(By.CSS_SELECTOR, "#content .product-thumb")

    assert heading.text.strip() == "Cameras"
    assert len(products) > 0, "Cameras should contain products"

    take_screenshot(driver, "TC-C02_S01_cameras")


def test_s2_open_subcategory(driver):
    """S02: Open Components > Monitors."""
    driver.get(BASE_URL)

    heading = open_subcategory(driver, "Components", "Monitors")

    assert heading.text.strip() == "Monitors"

    take_screenshot(driver, "TC-C02_S02_components_monitors")


def test_s3_open_empty_category(driver):
    """S03: Open Software category with no products."""
    driver.get(BASE_URL)

    heading = open_category(driver, "Software")
    products = driver.find_elements(By.CSS_SELECTOR, "#content .product-thumb")

    assert heading.text.strip() == "Software"
    assert len(products) == 0, "Software should not contain products"

    take_screenshot(driver, "TC-C02_S03_empty_software")
