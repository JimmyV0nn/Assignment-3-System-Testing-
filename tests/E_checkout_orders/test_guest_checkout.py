"""
TC-E01  Guest Checkout
Module: E - Checkout & Orders (Jimmy)

Precondition: not logged in; the cart holds one iPhone.
Scenario 1 - guest completes an order
  Steps: open Checkout, choose Guest Checkout, fill the billing details (Australia / New South Wales),
         keep Flat Shipping Rate, choose Cash On Delivery, accept the Terms & Conditions, Confirm Order
  Expected: redirect to checkout/success with "Your order has been placed!" and the cart is emptied
Scenario 2 - billing details left empty
  Steps: choose Guest Checkout and click Continue without filling the billing form
  Expected: a red message under every required field and the checkout does not move on to Step 4
Scenario 3 - Terms & Conditions not accepted
  Steps: complete Steps 1-4 as a guest, choose Cash On Delivery but leave the Terms box unticked, click Continue
  Expected: "Warning: You must agree to the Terms & Conditions!" and the Confirm Order button never appears
"""
from selenium.webdriver.common.by import By

from common.helpers import get_error_messages, take_screenshot, unique_email, wait_visible

from .checkout_steps import (
    ORDER_PLACED,
    PRODUCT,
    add_product_to_cart,
    choose_delivery_method,
    choose_guest_checkout,
    choose_payment_method,
    confirm_order,
    fill_billing_form,
    money,
    open_checkout,
    read_order_summary,
    submit_guest_details,
)


def _guest_checkout_until_payment(driver):
    add_product_to_cart(driver)
    open_checkout(driver)
    choose_guest_checkout(driver)
    fill_billing_form(driver, email=unique_email("guest"))
    submit_guest_details(driver)
    choose_delivery_method(driver)


def test_s1_guest_completes_order(driver):
    # Steps 1-5: guest details, delivery and payment
    _guest_checkout_until_payment(driver)
    choose_payment_method(driver)

    # Step 6: the summary lists the iPhone and its totals add up before confirming
    summary = read_order_summary(driver)
    take_screenshot(driver, "TC-E01_S1_confirm_step")
    assert [p["name"] for p in summary["products"]] == [PRODUCT["name"]]
    totals = summary["totals"]
    assert money(totals["Total"]) == money(totals["Sub-Total"]) + money(totals["Flat Shipping Rate"])

    # Confirm: the success page is shown and the cart is now empty
    heading = confirm_order(driver)
    take_screenshot(driver, "TC-E01_S1_order_placed")
    assert heading == ORDER_PLACED
    assert "0 item(s)" in driver.find_element(By.ID, "cart-total").text


def test_s2_guest_billing_details_required(driver):
    # Step 1: choose Guest Checkout, then submit the billing form empty
    add_product_to_cart(driver)
    open_checkout(driver)
    choose_guest_checkout(driver)
    submit_guest_details(driver)

    errors = get_error_messages(driver)
    take_screenshot(driver, "TC-E01_S2_required_fields")
    for expected in (
        "First Name must be between 1 and 32 characters!",
        "Last Name must be between 1 and 32 characters!",
        "E-Mail address does not appear to be valid!",
        "Telephone must be between 3 and 32 characters!",
        "Address 1 must be between 3 and 128 characters!",
        "City must be between 2 and 128 characters!",
        "Please select a region / state!",
    ):
        assert expected in errors, f"missing {expected!r} in {errors}"

    # The checkout stayed on Step 2: the Delivery Method step was not loaded
    assert not driver.find_elements(By.ID, "button-shipping-method")


def test_s3_terms_and_conditions_must_be_accepted(driver):
    # Steps 1-4 as a guest, then Step 5 without ticking the Terms & Conditions box
    _guest_checkout_until_payment(driver)
    choose_payment_method(driver, agree=False)

    warning = wait_visible(driver, (By.CSS_SELECTOR, "#collapse-payment-method .alert-danger"))
    take_screenshot(driver, "TC-E01_S3_terms_not_accepted")
    assert "You must agree to the Terms & Conditions!" in warning.text

    # The order cannot be confirmed: Step 6 was never loaded
    assert not driver.find_elements(By.ID, "button-confirm")
