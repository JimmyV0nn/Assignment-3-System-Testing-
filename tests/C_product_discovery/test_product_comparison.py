
"""
TC-C03: Product Comparison
Module: C - Product Discovery
Scenarios: S01, S02, S03
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.config import BASE_URL, url
from common.helpers import take_screenshot


def add_to_compare(driver, product_name):
    """Search for a product and add it to comparison."""
    driver.get(BASE_URL)

    search = driver.find_element(By.NAME, "search")
    search.send_keys(product_name, Keys.ENTER)

    wait = WebDriverWait(driver, 15)

    product = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            f"//div[contains(@class,'product-thumb')]"
            f"[.//a[normalize-space()='{product_name}']]"
        ))
    )

    product.find_element(
        By.CSS_SELECTOR, "button[onclick*='compare.add']"
    ).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".alert-success")
        )
    )


def open_comparison(driver):
    """Open the comparison page and return its content."""
    driver.get(url("product/compare"))

    return WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "content"))
    )


def test_s1_compare_two_products(driver):
    """S01: Compare two products."""
    add_to_compare(driver, "HTC Touch HD")
    add_to_compare(driver, "iPhone")

    content = open_comparison(driver)

    assert "HTC Touch HD" in content.text
    assert "iPhone" in content.text

    take_screenshot(driver, "TC-C03_S01_compare_two")


def test_s2_compare_three_products(driver):
    """S02: Compare three products."""
    add_to_compare(driver, "HTC Touch HD")
    add_to_compare(driver, "iPhone")
    add_to_compare(driver, "MacBook")

    content = open_comparison(driver)

    assert "HTC Touch HD" in content.text
    assert "iPhone" in content.text
    assert "MacBook" in content.text

    take_screenshot(driver, "TC-C03_S02_compare_three")



def test_s3_remove_product(driver):
    """TC-C03 S03: Remove HTC Touch HD from comparison."""
    add_to_compare(driver, "HTC Touch HD")
    add_to_compare(driver, "iPhone")

    content = open_comparison(driver)

    assert "HTC Touch HD" in content.text
    assert "iPhone" in content.text

    # Find HTC Touch HD's column in the comparison table.
    product_column = driver.find_element(
        By.XPATH,
        "//table[contains(@class,'table-bordered')]"
        "//tbody/tr[1]/td[a[normalize-space()='HTC Touch HD']]"
    )

    # Get the column position.
    column = driver.execute_script(
        "return Array.from(arguments[0].parentElement.children)"
        ".indexOf(arguments[0]) + 1;",
        product_column
    )

    # Click Remove in the same column.
    remove_button = driver.find_element(
        By.XPATH,
        f"//table[contains(@class,'table-bordered')]"
        f"//tbody/tr[last()]/td[{column}]"
        f"//a[contains(@href,'remove=')]"
    )

    remove_button.click()

    WebDriverWait(driver, 15).until(
        lambda d: "HTC Touch HD" not in
        d.find_element(By.ID, "content").text
    )

    content = driver.find_element(By.ID, "content")

    assert "HTC Touch HD" not in content.text
    assert "iPhone" in content.text

    take_screenshot(driver, "TC-C03_S03_remove_product")
