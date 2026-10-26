"""
TC-E03  Order History
Module: E - Checkout & Orders (Jimmy)

Precondition: a newly registered user is logged in (registered_user fixture).
Scenario 1 - new account with no orders
  Steps: open My Account > Order History (route=account/order)
  Expected: "You have not made any previous orders!" and no order rows
  Defect E-D1: the site shows "Your shopping cart is empty!" under the heading "Account" instead, so this
  scenario fails on purpose while the defect exists (same kind of defect as D-D1 on the empty wish list).
Scenario 2 - a placed order appears in the history
  Precondition: the user places one order (1 x iPhone, Cash On Delivery)
  Steps: open Order History
  Expected: exactly one order row, showing the same Total as the Confirm Order step and a status
Scenario 3 - order details
  Precondition: the user places one order
  Steps: open Order History and click View on the order
  Expected: the order information shows the iPhone, the delivery address, Cash On Delivery
            and Flat Shipping Rate
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import take_screenshot, wait_url_contains, wait_visible

from .checkout_steps import ADDRESS, PRODUCT, click, place_registered_order

NO_ORDERS = "You have not made any previous orders!"


def _order_rows(driver):
    driver.get(url("account/order"))
    wait_visible(driver, (By.ID, "content"))
    return driver.find_elements(By.CSS_SELECTOR, "#content table tbody tr")


def test_s1_no_orders_for_new_account(driver, registered_user):
    rows = _order_rows(driver)
    take_screenshot(driver, "TC-E03_S1_no_orders")
    assert rows == []
    # Defect E-D1: assert the correct text, so this fails while the site shows the cart message
    content = driver.find_element(By.ID, "content").text
    assert NO_ORDERS in content, (
        f"DEFECT E-D1: empty Order History shows {content!r} instead of {NO_ORDERS!r}"
    )


def test_s2_placed_order_is_listed(driver, registered_user):
    summary = place_registered_order(driver)

    rows = _order_rows(driver)
    take_screenshot(driver, "TC-E03_S2_order_listed")
    assert len(rows) == 1, f"Expected one order, found {len(rows)}"
    cells = [c.text.strip() for c in rows[0].find_elements(By.TAG_NAME, "td")]
    # Columns: Order ID, Customer, No. of Products, Status, Total, Date Added, View
    assert cells[0].startswith("#"), f"Order ID cell: {cells[0]!r}"
    assert cells[2] == "1", f"No. of Products: {cells[2]!r}"
    assert cells[3], "Order status should not be empty"
    assert cells[4] == summary["totals"]["Total"], f"History total {cells[4]} vs confirm total"


def test_s3_order_details(driver, registered_user):
    place_registered_order(driver)
    _order_rows(driver)

    # Open the order with its View button
    click(driver, (By.CSS_SELECTOR, "#content table tbody tr a[href*='account/order/info']"))
    wait_url_contains(driver, "account/order/info")
    details = wait_visible(driver, (By.ID, "content")).text
    take_screenshot(driver, "TC-E03_S3_order_details")

    for expected in (PRODUCT["name"], ADDRESS["address-1"], ADDRESS["city"],
                     "Cash On Delivery", "Flat Shipping Rate"):
        assert expected in details, f"{expected!r} missing from order details"
