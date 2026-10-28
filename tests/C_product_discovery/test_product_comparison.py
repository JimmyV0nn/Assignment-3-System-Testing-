  
"""
TC-C03  Product Comparison
Module: C - Product Discovery

Scenario 1 - compare two products
  Steps: add HTC Touch HD and iPhone, then open Product Comparison.
  Expected: both product names appear as columns in the comparison table.
Scenario 2 - compare three products
  Steps: add HTC Touch HD, iPhone, and MacBook, then open Product Comparison.
  Expected: all three product names appear as columns in the comparison table.
Scenario 3 - remove a compared product
  Steps: compare HTC Touch HD and iPhone, then remove HTC Touch HD.
  Expected: HTC Touch HD disappears from the table while iPhone remains.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.config import BASE_URL, url
from common.helpers import take_screenshot, wait_visible


def start_fresh(driver):
    """Start each scenario without products saved from previous tests."""
    driver.get(BASE_URL)
    driver.delete_all_cookies()
    driver.get(BASE_URL)


def add_to_compare(driver, product_name):
    """Find a product and add it to the comparison list."""
    driver.get(BASE_URL)
    search = wait_visible(driver, (By.NAME, "search"))
    search.clear()
    search.send_keys(product_name, Keys.ENTER)

    # Select the product card with the exact requested product name.
    product = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((
            By.XPATH,
            f"//div[contains(@class, 'product-thumb')]"
            f"[.//h4/a[normalize-space()='{product_name}']]"
        ))
    )
    product.find_element(By.CSS_SELECTOR, "button[onclick*='compare.add']").click()

    # The success alert confirms the add action was accepted.
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )


def comparison_names(driver):
    """Read only the Product row in the comparison table."""
    product_row = wait_visible(driver, (
        By.XPATH,
        "//div[@id='content']//table//tr[td[1][normalize-space()='Product']]"
    ))
    # Skip the first cell ('Product'); the others are product columns.
    return [cell.text.strip() for cell in product_row.find_elements(By.XPATH, "./td[position()>1]")]


def open_comparison(driver):
    driver.get(url("product/compare"))
    wait_visible(driver, (By.ID, "content"))
    return comparison_names(driver)


def test_s1_compare_two_products(driver):
    # Input: two products; expected: two matching comparison columns.
    start_fresh(driver)
    add_to_compare(driver, "HTC Touch HD")
    add_to_compare(driver, "iPhone")
    names = open_comparison(driver)

    take_screenshot(driver, "TC-C03_S1_compare_two")
    assert len(names) == 2 and all(
        name in names for name in ("HTC Touch HD", "iPhone")
    ), f"Expected two products in comparison table; found: {names}"


def test_s2_compare_three_products(driver):
    # Input: three products; expected: three matching comparison columns.
    start_fresh(driver)
    for name in ("HTC Touch HD", "iPhone", "MacBook"):
        add_to_compare(driver, name)
    names = open_comparison(driver)

    take_screenshot(driver, "TC-C03_S2_compare_three")
    assert len(names) == 3 and all(
        name in names for name in ("HTC Touch HD", "iPhone", "MacBook")
    ), f"Expected three products in comparison table; found: {names}"


def test_s3_remove_product(driver):
    # Input: remove HTC Touch HD; expected: iPhone remains.
    start_fresh(driver)
    add_to_compare(driver, "HTC Touch HD")
    add_to_compare(driver, "iPhone")
    names = open_comparison(driver)
    assert "HTC Touch HD" in names and "iPhone" in names

    # The Remove buttons are in the product columns, not a row labelled Remove.
    # Match the product column (first column is the row label).
    column = names.index("HTC Touch HD") + 2
    remove_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@id='content']//table"
            f"//tr/td[{column}]//a[contains(@class, 'btn-danger')]"
        ))
    )
    remove_button.click()

    WebDriverWait(driver, 15).until(
        lambda d: "HTC Touch HD" not in comparison_names(d)
    )
    names = comparison_names(driver)
    take_screenshot(driver, "TC-C03_S3_remove_product")
    assert names == ["iPhone"], f"Expected only iPhone after removal; found: {names}"
