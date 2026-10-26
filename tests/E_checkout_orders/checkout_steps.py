"""Reusable steps for Module E: filling the cart and walking the 6-step OpenCart checkout.

The checkout page is one page with six AJAX panels; each Continue button loads the next panel,
so every step waits for the next panel's button before moving on.
"""
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from common.config import DEFAULT_TIMEOUT, url
from common.helpers import fill, js_click, wait_clickable, wait_url_contains, wait_visible

PRODUCT = {"product_id": 40, "name": "iPhone"}

# Australian address: prices are shown without UK VAT, and Australia does not require a postcode
ADDRESS = {
    "firstname": "Jimmy",
    "lastname": "Tester",
    "telephone": "0400000000",
    "address-1": "15 Broadway",
    "city": "Ultimo",
    "postcode": "2007",
}
COUNTRY = "Australia"
REGION = "New South Wales"

ORDER_PLACED = "Your order has been placed!"


def wait_ajax_idle(driver):
    """Wait until the page's jQuery AJAX calls have finished.

    Each checkout step saves to the server and reloads other panels in the background. Clicking the next
    step before those calls finish can leave the server's checkout session half-updated
    (e.g. "Warning: Payment method required!" although Cash On Delivery is selected).
    """
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        lambda d: d.execute_script("return !window.jQuery || jQuery.active === 0")
    )


def click(driver, locator):
    """Click once background AJAX has settled and the element is clickable.

    Falls back to a JS click if a panel animation covers the element.
    """
    wait_ajax_idle(driver)
    element = wait_clickable(driver, locator)
    try:
        element.click()
    except ElementClickInterceptedException:
        js_click(driver, element)


# ---------- cart ----------

def add_product_to_cart(driver, product=PRODUCT):
    """Add one unit of the product from its product page and wait for the confirmation."""
    driver.get(url(f"product/product&product_id={product['product_id']}"))
    click(driver, (By.ID, "button-cart"))
    alert = wait_visible(driver, (By.CSS_SELECTOR, ".alert-success"))
    assert product["name"] in alert.text, f"Add to cart failed: {alert.text}"


def open_checkout(driver):
    driver.get(url("checkout/checkout"))


# ---------- step 1-2: checkout option and billing details ----------

def choose_guest_checkout(driver):
    """Step 1: pick Guest Checkout and continue to the guest billing form."""
    click(driver, (By.CSS_SELECTOR, "input[name='account'][value='guest']"))
    click(driver, (By.ID, "button-account"))
    wait_visible(driver, (By.ID, "input-payment-firstname"))


def _wait_region_loaded(driver, region=None):
    """Wait for the AJAX region list; it reloads when the form opens and whenever the country changes."""
    def loaded(d):
        options = [o.text for o in Select(d.find_element(By.ID, "input-payment-zone")).options]
        return len(options) > 1 if region is None else region in options

    WebDriverWait(driver, DEFAULT_TIMEOUT, ignored_exceptions=(StaleElementReferenceException,)).until(loaded)


def fill_billing_form(driver, email=None):
    """Step 2: fill the billing address form (guest form when email is given, otherwise logged-in form)."""
    _wait_region_loaded(driver)
    fill(driver, (By.ID, "input-payment-firstname"), ADDRESS["firstname"])
    fill(driver, (By.ID, "input-payment-lastname"), ADDRESS["lastname"])
    if email is not None:
        fill(driver, (By.ID, "input-payment-email"), email)
        fill(driver, (By.ID, "input-payment-telephone"), ADDRESS["telephone"])
    fill(driver, (By.ID, "input-payment-address-1"), ADDRESS["address-1"])
    fill(driver, (By.ID, "input-payment-city"), ADDRESS["city"])
    fill(driver, (By.ID, "input-payment-postcode"), ADDRESS["postcode"])
    Select(driver.find_element(By.ID, "input-payment-country")).select_by_visible_text(COUNTRY)
    _wait_region_loaded(driver, REGION)
    Select(driver.find_element(By.ID, "input-payment-zone")).select_by_visible_text(REGION)


def submit_guest_details(driver):
    """Step 2 (guest): Continue. Delivery address = billing address, so Step 3 is skipped."""
    click(driver, (By.ID, "button-guest"))


def submit_registered_addresses(driver):
    """Step 2-3 (logged in): save the new billing address, then keep it as the delivery address."""
    click(driver, (By.ID, "button-payment-address"))
    click(driver, (By.ID, "button-shipping-address"))


# ---------- step 4-6: delivery, payment, confirm ----------

def choose_delivery_method(driver):
    """Step 4: keep Flat Shipping Rate (pre-selected) and continue."""
    click(driver, (By.ID, "button-shipping-method"))


def choose_payment_method(driver, agree=True):
    """Step 5: pick Cash On Delivery, optionally accept the Terms & Conditions, and continue."""
    click(driver, (By.CSS_SELECTOR, "#collapse-payment-method input[name='payment_method'][value='cod']"))
    if agree:
        click(driver, (By.CSS_SELECTOR, "#collapse-payment-method input[name='agree']"))
    click(driver, (By.ID, "button-payment-method"))


def read_order_summary(driver):
    """Step 6: return the products and totals shown before the order is confirmed."""
    wait_visible(driver, (By.ID, "button-confirm"))
    wait_ajax_idle(driver)
    table =driver.find_element(By.CSS_SELECTOR, "#collapse-checkout-confirm table")
    products = []
    for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
        cells = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
        products.append({"name": cells[0], "model": cells[1], "quantity": int(cells[2]),
                         "unit_price": cells[3], "total": cells[4]})
    totals = {}
    for row in table.find_elements(By.CSS_SELECTOR, "tfoot tr"):
        label, value = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
        totals[label.rstrip(":")] = value
    return {"products": products, "totals": totals}


def confirm_order(driver):
    """Step 6: Confirm Order and return the heading of the success page."""
    click(driver, (By.ID, "button-confirm"))
    wait_url_contains(driver, "checkout/success")
    return wait_visible(driver, (By.CSS_SELECTOR, "#content h1")).text


def money(text):
    """Turn '$1,106.00' into 1106.00 so totals can be added up."""
    return float(text.replace("$", "").replace(",", ""))


# ---------- complete flows (used as preconditions) ----------

def place_registered_order(driver):
    """Logged-in user: add the product and complete checkout. Returns the confirm-step summary."""
    add_product_to_cart(driver)
    open_checkout(driver)
    wait_visible(driver, (By.ID, "input-payment-firstname"))
    fill_billing_form(driver)
    submit_registered_addresses(driver)
    choose_delivery_method(driver)
    choose_payment_method(driver)
    summary = read_order_summary(driver)
    assert confirm_order(driver) == ORDER_PLACED
    return summary
