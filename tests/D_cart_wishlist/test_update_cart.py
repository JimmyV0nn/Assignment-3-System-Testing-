"""Test case D_TC02 - Update Shopping Cart.

Scenario 1: increase the quantity of a cart line.
Scenario 2: decrease the quantity of a cart line.
Scenario 3: remove the only product so the cart becomes empty.
"""

import pytest

from . import helpers
from .helpers import IPHONE


def _cart_with_iphone(driver, quantity):
    """Precondition helper: fill the cart from the product page."""
    helpers.open_cart(driver)
    assert helpers.cart_is_empty(driver), "Precondition failed: the cart was not empty at the start"
    for index in range(1, quantity + 1):
        helpers.add_to_cart_from_product_page(
            driver, IPHONE["product_id"], 1, expected_count=index
        )


@pytest.mark.scenario("D_TC02_S1", "Increase iPhone quantity from 1 to 2")
def test_increase_quantity(driver, shots):
    _cart_with_iphone(driver, 1)
    helpers.open_cart(driver)
    shots.capture("01_cart_before_update")

    before = helpers.find_cart_row(driver, IPHONE["name"])
    assert before["quantity"] == 1, f"Precondition quantity: {before['quantity']}"

    alert = helpers.update_cart_quantity(driver, IPHONE["name"], 2)
    shots.capture("02_update_success_message")
    assert "modified your shopping cart" in alert.lower(), f"Update confirmation text: {alert}"

    # Reload the cart from the server so the saved value is checked, not the
    # value that was typed into the still unsubmitted input.
    helpers.open_cart(driver)
    shots.capture("03_cart_after_update")

    rows = helpers.cart_rows(driver)
    assert len(rows) == 1, f"Expected one cart line, found {[row['name'] for row in rows]}"
    row = rows[0]
    assert row["quantity"] == 2, f"Saved quantity after reload: {row['quantity']}"
    assert row["unit_price"] == IPHONE["price"], f"Unit price: {row['unit_price']}"
    assert row["line_total"] == IPHONE["price"] * 2, f"Line total: {row['line_total']}"

    totals = helpers.cart_totals(driver)
    helpers.assert_totals_match_rows(rows, totals)
    assert totals["Total"] == IPHONE["price"] * 2, f"Cart total: {totals['Total']}"


@pytest.mark.scenario("D_TC02_S2", "Decrease iPhone quantity from 2 to 1")
def test_decrease_quantity(driver, shots):
    _cart_with_iphone(driver, 2)
    helpers.open_cart(driver)
    shots.capture("01_cart_before_update")

    before = helpers.find_cart_row(driver, IPHONE["name"])
    assert before["quantity"] == 2, f"Precondition quantity: {before['quantity']}"

    alert = helpers.update_cart_quantity(driver, IPHONE["name"], 1)
    shots.capture("02_update_success_message")
    assert "modified your shopping cart" in alert.lower(), f"Update confirmation text: {alert}"

    helpers.open_cart(driver)
    shots.capture("03_cart_after_update")

    rows = helpers.cart_rows(driver)
    assert len(rows) == 1, f"Expected one cart line, found {[row['name'] for row in rows]}"
    row = rows[0]
    assert row["quantity"] == 1, f"Saved quantity after reload: {row['quantity']}"
    assert row["line_total"] == IPHONE["price"], f"Line total: {row['line_total']}"

    totals = helpers.cart_totals(driver)
    helpers.assert_totals_match_rows(rows, totals)
    assert totals["Total"] == IPHONE["price"], f"Cart total: {totals['Total']}"


@pytest.mark.scenario("D_TC02_S3", "Remove the only product and empty the cart")
def test_remove_product(driver, shots):
    _cart_with_iphone(driver, 1)
    helpers.open_cart(driver)
    shots.capture("01_cart_before_remove")
    assert len(helpers.cart_rows(driver)) == 1, "Precondition failed: expected exactly one cart line"

    helpers.remove_cart_row(driver, IPHONE["name"])
    shots.capture("02_cart_after_remove")

    assert helpers.cart_rows(driver) == [], f"Cart still has lines: {helpers.cart_rows(driver)}"
    assert helpers.cart_is_empty(driver), "The empty-cart message 'Your shopping cart is empty!' is missing"

    page_text = helpers.body_text(driver)
    assert "Your shopping cart is empty!" in page_text, (
        "Empty cart confirmation text not found after removing the product"
    )
    helpers.note("the site does not show a success banner for removing a product; only the empty-cart message")
