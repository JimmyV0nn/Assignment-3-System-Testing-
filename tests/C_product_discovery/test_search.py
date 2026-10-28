
"""
TC-C01  Product Search
Module: C - Product Discovery

Scenario 1 - search with exact product name
  Steps: enter "HTC Touch HD" in the search box and submit.
  Expected: "HTC Touch HD" appears as a product in the search results.
Scenario 2 - search with nonexistent product name
  Steps: enter "sth_not_existing" in the search box and submit.
  Expected: no product cards appear in the search results.
Scenario 3 - search with partial product name
  Steps: enter "HTC" in the search box and submit.
  Expected: "HTC Touch HD" appears as a product in the search results.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from common.config import BASE_URL
from common.helpers import take_screenshot, wait_visible


def search_products(driver, keyword):
    """Submit a search and return the results area."""
    driver.get(BASE_URL)
    search_box = wait_visible(driver, (By.NAME, "search"))
    search_box.clear()
    search_box.send_keys(keyword, Keys.ENTER)

    # Wait for navigation to the product search page.
    WebDriverWait(driver, 15).until(
        lambda d: "route=product/search" in d.current_url
    )
    return wait_visible(driver, (By.ID, "content"))


def product_names(content):
    """Read product names from actual product cards."""
    return [
        link.text.strip()
        for link in content.find_elements(
            By.CSS_SELECTOR, ".product-thumb h4 a"
        )
    ]


def test_s1_search_exact_name(driver):
    # Exact keyword should return the requested product.
    content = search_products(driver, "HTC Touch HD")
    names = product_names(content)

    take_screenshot(driver, "TC-C01_S1_exact_name")
    assert "HTC Touch HD" in names, \
        f"Product not found; results: {names}"


def test_s2_search_nonexistent_name(driver):
    # Invalid keyword should return no product cards.
    content = search_products(driver, "sth_not_existing")
    names = product_names(content)

    take_screenshot(driver, "TC-C01_S2_no_results")
    assert names == [], \
        f"Expected no products; results: {names}"


def test_s3_search_partial_name(driver):
    # Partial keyword should still return HTC Touch HD.
    content = search_products(driver, "HTC")
    names = product_names(content)

    take_screenshot(driver, "TC-C01_S3_partial_name")
    assert "HTC Touch HD" in names, \
        f"Product not found; results: {names}"
