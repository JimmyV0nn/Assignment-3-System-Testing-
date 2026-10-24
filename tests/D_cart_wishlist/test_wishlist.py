"""Test case TC-D03 - Wishlist.

Every scenario runs with a throw-away account created as preparation, so the
student's personal account is never touched. Scenario 1: add to wish list.
Scenario 2: remove from wish list. Scenario 3: move an item from the wish
list to the cart.
"""

import pytest

from . import helpers
from .helpers import IPHONE


@pytest.mark.scenario("TC-D03-S1", "Add iPhone to an empty wish list")
def test_add_to_wishlist(driver, account, shots):
    helpers.ensure_logged_in(driver, account)

    # Precondition: wish list is empty.
    helpers.clear_wishlist(driver)
    helpers.open_wishlist(driver)
    assert helpers.wishlist_rows(driver) == [], "Precondition failed: the wish list was not empty"
    shots.capture("01_wishlist_empty_before")
    # Defect: the empty wish list page shows the cart-empty message instead of
    # a wish-list-empty message. The test asserts the correct text, so it fails
    # while the site is defective.
    content = driver.find_element("css selector", "#content").text.lower()
    assert "your wish list is empty" in content, (
        "DEFECT: empty wish list shows 'Your shopping cart is empty!' "
        "instead of a wish-list-empty message"
    )

    details = helpers.open_product_page(driver, IPHONE["product_id"])
    shots.capture("02_product_page_before_wishlist")
    assert details["price"] == IPHONE["price"], (
        f"Price changed on the site: product page shows {details['price']}, "
        f"configured expectation is {IPHONE['price']}"
    )

    toast = helpers.add_to_wishlist_from_product_page(driver, IPHONE["product_id"])
    assert IPHONE["name"] in toast, f"Wish list confirmation text: {toast}"
    shots.capture("03_wishlist_confirmation")

    helpers.open_wishlist(driver)
    shots.capture("04_wishlist_after_add")

    rows = helpers.wishlist_rows(driver)
    assert len(rows) == 1, f"Expected one wish list line, found {[row['name'] for row in rows]}"
    row = rows[0]
    assert row["name"] == IPHONE["name"], f"Wish list product name: {row['name']}"
    assert row["model"] == IPHONE["model"], f"Wish list product code: {row['model']}"
    assert row["unit_price"] == IPHONE["price"], f"Wish list unit price: {row['unit_price']}"
    assert "in stock" in row["stock"].lower(), f"Wish list stock status: {row['stock']}"


@pytest.mark.scenario("TC-D03-S2", "Remove iPhone from the wish list")
def test_remove_from_wishlist(driver, account, shots):
    helpers.ensure_logged_in(driver, account)

    # Precondition: wish list contains iPhone only.
    helpers.clear_wishlist(driver)
    helpers.add_to_wishlist_from_product_page(driver, IPHONE["product_id"])
    helpers.open_wishlist(driver)
    shots.capture("01_wishlist_before_remove")
    assert len(helpers.wishlist_rows(driver)) == 1, (
        f"Precondition failed: {[row['name'] for row in helpers.wishlist_rows(driver)]}"
    )

    alert = helpers.remove_wishlist_item(driver, IPHONE["name"])
    shots.capture("02_remove_success_message")
    assert "modified your wish list" in alert.lower(), f"Remove confirmation text: {alert}"

    rows = helpers.wishlist_rows(driver)
    assert rows == [], f"Wish list still contains: {[row['name'] for row in rows]}"
    shots.capture("03_wishlist_after_remove")
    # Defect: after removal the wish list shows the cart-empty message instead
    # of a wish-list-empty message; the test asserts the correct text.
    content = driver.find_element("css selector", "#content").text.lower()
    assert "your wish list is empty" in content, (
        "DEFECT: empty wish list shows 'Your shopping cart is empty!' "
        "instead of a wish-list-empty message"
    )


@pytest.mark.scenario("TC-D03-S3", "Add iPhone from the wish list to an empty cart")
def test_wishlist_item_to_cart(driver, account, shots):
    helpers.ensure_logged_in(driver, account)

    # Precondition: wish list holds iPhone and the cart is empty.
    helpers.clear_wishlist(driver)
    helpers.add_to_wishlist_from_product_page(driver, IPHONE["product_id"])
    helpers.open_cart(driver)
    assert helpers.cart_is_empty(driver), "Precondition failed: the cart was not empty at the start"
    shots.capture("01_empty_cart_before")

    helpers.open_wishlist(driver)
    shots.capture("02_wishlist_before_add_to_cart")
    assert helpers.find_wishlist_row(driver, IPHONE["name"])["name"] == IPHONE["name"]

    toast = helpers.add_wishlist_item_to_cart(driver, IPHONE["name"], expected_cart_count=1)
    shots.capture("03_add_to_cart_confirmation")
    assert IPHONE["name"] in toast, f"Add-to-cart confirmation text: {toast}"

    helpers.open_cart(driver)
    shots.capture("04_cart_after_wishlist_add")

    rows = helpers.cart_rows(driver)
    assert len(rows) == 1, f"Expected one cart line, found {[row['name'] for row in rows]}"
    row = rows[0]
    assert row["name"] == IPHONE["name"], f"Cart line name: {row['name']}"
    assert row["quantity"] == 1, f"Cart line quantity: {row['quantity']}"
    assert row["unit_price"] == IPHONE["price"], f"Unit price: {row['unit_price']}"
    assert row["line_total"] == IPHONE["price"], f"Line total: {row['line_total']}"

    totals = helpers.cart_totals(driver)
    helpers.assert_totals_match_rows(rows, totals)
    assert totals["Total"] == IPHONE["price"], f"Cart total: {totals['Total']}"

    # Only informational: this scenario verifies the cart, not that the wish
    # list entry is removed automatically.
    helpers.open_wishlist(driver)
    still_listed = [row["name"] for row in helpers.wishlist_rows(driver)]
    helpers.note(f"after adding to the cart the wish list still shows: {still_listed}")
