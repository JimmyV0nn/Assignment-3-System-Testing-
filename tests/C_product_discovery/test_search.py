
"""
TC-C01: Product Search
Module: C - Product Discovery
Scenarios: S01, S02, S03
"""

from urllib.parse import parse_qs, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from common.config import BASE_URL
from common.helpers import (
    fill,
    take_screenshot,
    wait_visible,
)


def perform_search(driver, keyword):
    """Search using the website's visible search field."""
    driver.get(BASE_URL)

    search_box = fill(
        driver,
        (By.NAME, "search"),
        keyword
    )
    search_box.send_keys(Keys.ENTER)

    # Wait until the submitted search reaches the results route.
    def correct_search_url(browser):
        current = browser.current_url or ""
        parameters = parse_qs(urlparse(current).query)

        return (
            parameters.get("route", [""])[0] == "product/search"
            and parameters.get("search", [""])[0] == keyword
        )

    WebDriverWait(driver, 15).until(
        correct_search_url,
        message=f"Search did not navigate for: {keyword}"
    )

    return wait_visible(
        driver,
        (By.CSS_SELECTOR, "#content")
    )


def test_s1_search_full_keyword(driver):
    """TC-C01 S01: Search for a complete product name."""
    content = perform_search(driver, "HTC Touch HD")

    assert "HTC Touch HD" in content.text, (
        "Expected product HTC Touch HD was not found"
    )

    take_screenshot(
        driver,
        "TC-C01_S01_full_keyword"
    )


def test_s2_search_nonexistent_keyword(driver):
    """TC-C01 S02: Search for a nonexistent product."""
    content = perform_search(driver, "sth_not_existing")

    products = content.find_elements(By.CSS_SELECTOR, ".product-thumb")

    assert len(products) == 0, (
        "Expected no matching products, but products were found"
    )

    take_screenshot(
        driver,
        "TC-C01_S02_no_matching_products"
    )


def test_s3_search_partial_keyword(driver):
    """TC-C01 S03: Search using a partial keyword."""
    content = perform_search(driver, "HTC")

    assert "HTC Touch HD" in content.text, (
        "Partial keyword did not return the expected product"
    )

    take_screenshot(
        driver,
        "TC-C01_S03_partial_keyword"
    )
