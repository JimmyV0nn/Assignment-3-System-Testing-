"""Test case D_TC01 - Add to Cart.

Scenario 1: add one MacBook Pro to an empty cart.
Scenario 2: add the same MacBook Pro twice.
Scenario 3: add a different product (iPhone) next to MacBook Pro x2.
"""

import pytest

from . import helpers
from .helpers import IPHONE, MACBOOK


@pytest.mark.scenario("D_TC01_S1", "Add a single MacBook Pro to an empty cart")
def test_add_single_item_to_empty_cart(driver, shots):
    # Precondition: a fresh browser session with an empty cart.
    helpers.open_cart(driver)
    assert helpers.cart_is_empty(driver), "Precondition failed: the cart was not empty at the start"
    shots.capture("01_empty_cart_before")

    details = helpers.open_product_page(driver, MACBOOK["product_id"])
    shots.capture("02_product_page_before_add")
    assert details["name"] == MACBOOK["name"], f"Product name on page: {details['name']}"
    assert details["model"] == MACBOOK["model"], f"Product code on page: {details['model']}"
    assert details["price"] == MACBOOK["price"], (
        f"Price changed on the site: product page shows {details['price']}, "
        f"configured expectation is {MACBOOK['price']}"
    )

    toast = helpers.add_to_cart_from_product_page(
        driver, MACBOOK["product_id"], quantity=1, expected_count=1
    )
    assert MACBOOK["name"] in toast, f"Unexpected confirmation text: {toast}"
    shots.capture("03_add_to_cart_confirmation")

    helpers.open_cart(driver)
    shots.capture("04_cart_after_add")

    rows = helpers.cart_rows(driver)
    assert len(rows) == 1, f"Expected one cart line, found {[row['name'] for row in rows]}"
    row = rows[0]
    assert row["name"] == MACBOOK["name"], f"Cart line name: {row['name']}"
    assert row["model"] == MACBOOK["model"], f"Cart line model: {row['model']}"
    assert row["quantity"] == 1, f"Cart line quantity: {row['quantity']}"
    assert row["unit_price"] == MACBOOK["price"], f"Unit price: {row['unit_price']}"
    assert row["line_total"] == MACBOOK["price"], f"Line total: {row['line_total']}"

    totals = helpers.cart_totals(driver)
    helpers.assert_totals_match_rows(rows, totals)
    assert totals["Total"] == MACBOOK["price"], f"Cart total: {totals['Total']}"
    helpers.note(f"screenshot evidence and totals: {totals}")


@pytest.mark.scenario("D_TC01_S2", "Add the same MacBook Pro twice from the product page")
def test_add_same_item_twice(driver, shots):
    helpers.open_cart(driver)
    assert helpers.cart_is_empty(driver), "Precondition failed: the cart was not empty at the start"
    shots.capture("01_empty_cart_before")

    details = helpers.open_product_page(driver, MACBOOK["product_id"])
    shots.capture("02_product_page_quantity_1")
    assert details["price"] == MACBOOK["price"], (
        f"Price changed on the site: product page shows {details['price']}, "
        f"configured expectation is {MACBOOK['price']}"
    )

    # Each click is followed by a wait for its own confirmation, so a fast
    # double click can never hide a lost add request.
    first = helpers.add_to_cart_from_product_page(
        driver, MACBOOK["product_id"], quantity=1, expected_count=1
    )
    shots.capture("03_first_add_confirmed")
    assert MACBOOK["name"] in first, f"First confirmation text: {first}"

    second = helpers.add_to_cart_from_product_page(
        driver, MACBOOK["product_id"], quantity=1, expected_count=2
    )
    shots.capture("04_second_add_confirmed")
    assert MACBOOK["name"] in second, f"Second confirmation text: {second}"

    helpers.open_cart(driver)
    shots.capture("05_cart_after_two_adds")

    rows = helpers.cart_rows(driver)
    assert len(rows) == 1, f"Expected one merged line for the same product, found {[row['name'] for row in rows]}"
    row = rows[0]
    assert row["name"] == MACBOOK["name"], f"Cart line name: {row['name']}"
    assert row["quantity"] == 2, f"Quantity after two adds: {row['quantity']}"
    assert row["line_total"] == MACBOOK["price"] * 2, f"Line total: {row['line_total']}"

    totals = helpers.cart_totals(driver)
    helpers.assert_totals_match_rows(rows, totals)
    assert totals["Total"] == MACBOOK["price"] * 2, f"Cart total: {totals['Total']}"


@pytest.mark.scenario("D_TC01_S3", "Add a different product (iPhone) to a cart holding MacBook Pro x2")
def test_add_different_product(driver, shots):
    helpers.open_cart(driver)
    assert helpers.cart_is_empty(driver), "Precondition failed: the cart was not empty at the start"
    shots.capture("01_empty_cart_before")

    helpers.add_to_cart_from_product_page(driver, MACBOOK["product_id"], 1, expected_count=1)
    helpers.add_to_cart_from_product_page(driver, MACBOOK["product_id"], 1, expected_count=2)
    helpers.open_cart(driver)
    shots.capture("02_cart_with_macbook_two")

    # The iPhone link is discovered through the search page, not guessed.
    iphone_id, iphone_details = helpers.find_iphone_product_id(driver)
    shots.capture("03_iphone_product_page")
    assert iphone_details["name"] == IPHONE["name"], f"iPhone page title: {iphone_details['name']}"
    assert iphone_details["model"] == IPHONE["model"], (
        f"iPhone product code on page: {iphone_details['model']}"
    )
    assert iphone_details["price"] == IPHONE["price"], (
        f"Price changed on the site: iPhone shows {iphone_details['price']}, "
        f"configured expectation is {IPHONE['price']}"
    )

    toast = helpers.add_to_cart_from_product_page(driver, iphone_id, 1, expected_count=3)
    shots.capture("04_iphone_add_confirmed")
    assert IPHONE["name"] in toast, f"iPhone confirmation text: {toast}"

    helpers.open_cart(driver)
    shots.capture("05_cart_with_two_products")

    rows = helpers.cart_rows(driver)
    assert len(rows) == 2, f"Expected two cart lines, found {[row['name'] for row in rows]}"

    macbook_row = next((row for row in rows if row["name"] == MACBOOK["name"]), None)
    iphone_row = next((row for row in rows if row["name"] == IPHONE["name"]), None)
    assert macbook_row is not None, f"MacBook Pro missing from cart: {[row['name'] for row in rows]}"
    assert iphone_row is not None, f"iPhone missing from cart: {[row['name'] for row in rows]}"

    assert macbook_row["quantity"] == 2, f"MacBook Pro quantity: {macbook_row['quantity']}"
    assert macbook_row["line_total"] == MACBOOK["price"] * 2, f"MacBook Pro line total: {macbook_row['line_total']}"
    assert iphone_row["quantity"] == 1, f"iPhone quantity: {iphone_row['quantity']}"
    assert iphone_row["unit_price"] == IPHONE["price"], f"iPhone unit price: {iphone_row['unit_price']}"
    assert iphone_row["line_total"] == IPHONE["price"], f"iPhone line total: {iphone_row['line_total']}"

    totals = helpers.cart_totals(driver)
    helpers.assert_totals_match_rows(rows, totals)
    expected_total = MACBOOK["price"] * 2 + IPHONE["price"]
    assert totals["Total"] == expected_total, (
        f"Cart total {totals['Total']} does not equal the expected {expected_total}"
    )
    # The site lists tax separately from Sub-Total, so the whole breakdown is logged.
    helpers.note(f"displayed cart breakdown: {totals}")
