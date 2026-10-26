"""
TC-E02  Registered Checkout
Module: E - Checkout & Orders (Jimmy)

Precondition: a newly registered user is logged in (registered_user fixture) and has no saved address.
Scenario 1 - logged-in user completes an order
  Steps: add an iPhone to the cart, open Checkout, enter a new billing address, keep it as the delivery
         address, keep Flat Shipping Rate, choose Cash On Delivery, accept the Terms, Confirm Order
  Expected: Step 1 (Checkout Options) is skipped, the order is placed ("Your order has been placed!")
            and the address is saved to the user's Address Book
Scenario 2 - checkout with an empty cart
  Steps: open Checkout without adding anything to the cart
  Expected: redirect to the Shopping Cart page with "Your shopping cart is empty!"
Scenario 3 - order summary before confirming
  Steps: add an iPhone, complete Steps 2-5, stop at Step 6 (Confirm Order)
  Expected: the summary lists 1 x iPhone, and Total = Sub-Total + Flat Shipping Rate
"""
from selenium.webdriver.common.by import By

from common.config import url
from common.helpers import take_screenshot, wait_url_contains, wait_visible

from .checkout_steps import (
    ADDRESS,
    ORDER_PLACED,
    PRODUCT,
    add_product_to_cart,
    choose_delivery_method,
    choose_payment_method,
    confirm_order,
    fill_billing_form,
    money,
    open_checkout,
    read_order_summary,
    submit_registered_addresses,
)


def _registered_checkout_until_confirm(driver):
    add_product_to_cart(driver)
    open_checkout(driver)
    # A logged-in user starts at Step 2; with no saved address the new-address form is shown
    wait_visible(driver, (By.ID, "input-payment-firstname"))
    assert not driver.find_elements(By.ID, "button-account"), "Step 1 should be skipped when logged in"
    fill_billing_form(driver)
    submit_registered_addresses(driver)
    choose_delivery_method(driver)
    choose_payment_method(driver)
    return read_order_summary(driver)


def test_s1_registered_user_completes_order(driver, registered_user):
    _registered_checkout_until_confirm(driver)
    take_screenshot(driver, "TC-E02_S1_confirm_step")

    heading = confirm_order(driver)
    take_screenshot(driver, "TC-E02_S1_order_placed")
    assert heading == ORDER_PLACED

    # The address entered during checkout was saved to the Address Book
    driver.get(url("account/address"))
    book = wait_visible(driver, (By.ID, "content")).text
    assert ADDRESS["address-1"] in book and ADDRESS["city"] in book


def test_s2_checkout_with_empty_cart(driver, registered_user):
    # Open Checkout with nothing in the cart
    open_checkout(driver)

    wait_url_contains(driver, "checkout/cart")
    content = wait_visible(driver, (By.ID, "content")).text
    take_screenshot(driver, "TC-E02_S2_empty_cart_redirect")
    assert "Your shopping cart is empty!" in content


def test_s3_order_summary_totals(driver, registered_user):
    summary = _registered_checkout_until_confirm(driver)
    take_screenshot(driver, "TC-E02_S3_order_summary")

    assert len(summary["products"]) == 1, summary["products"]
    product = summary["products"][0]
    assert product["name"] == PRODUCT["name"]
    assert product["quantity"] == 1
    assert product["total"] == product["unit_price"]

    totals = summary["totals"]
    assert money(totals["Sub-Total"]) == money(product["total"])
    assert money(totals["Total"]) == money(totals["Sub-Total"]) + money(totals["Flat Shipping Rate"]), totals
