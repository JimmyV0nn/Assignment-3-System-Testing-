# Defect Log

Defects found by the automated system tests on <https://opencart.abstracta.us/>.
D-D1 and E-D1 are backed by tests that assert the **correct** behaviour, so those tests fail while
the defect exists and will pass once the site is fixed. D1 and E-D2 were found in the tests'
results and screenshots without failing a test. Evidence screenshots are in `screenshots/defects/`.

## Summary

| ID | Module | Test case / scenario | Severity | Summary | Status |
|---|---|---|---|---|---|
| D1 | A. Account Basics | TC-A03 Forgotten Password, S1 | Low | Success message is ungrammatical ("sent your email address") | Open |
| D-D1 | D. Shopping Cart & Wishlist | TC-D03 Wishlist, S1 and S2 | Medium | Empty wish list shows the shopping-cart message and heading "Account" | Open |
| E-D1 | E. Checkout & Orders | TC-E03 Order History, S1 | Medium | Empty Order History shows the shopping-cart message and heading "Account" | Open |
| E-D2 | E. Checkout & Orders | TC-E03 Order History, S3 (screenshot) | Low | Order details show "Order ID: #%s #32944": an unfilled format placeholder | Open |

Severity scale: **High** – blocks a core task; **Medium** – the user is given wrong or misleading
information but can still complete the task; **Low** – cosmetic (wording, layout).

Expected full-suite result while these defects are open: **45 tests, 42 passed, 3 failed**
(TC-D03 S1, TC-D03 S2, TC-E03 S1). D1 and E-D2 do not fail a test: TC-A03 S1 only checks the
opening phrase of the message, and TC-E03 S3 does not check the Order ID line.

---

## D1 – Forgotten Password success message is ungrammatical

- **Found by:** TC-A03 Forgotten Password, Scenario 1 (`tests/A_account_basics/test_forgotten_password.py`)
- **Severity:** Low (cosmetic wording)
- **Steps to reproduce:**
  1. Register an account with email E, then log out.
  2. Open My Account > Forgotten Password (`route=account/forgotten`).
  3. Enter E and click Continue.
- **Expected:** "An email with a confirmation link has been sent **to** your email address."
- **Actual:** "An email with a confirmation link has been sent your email address." (the word "to" is missing)
- **Evidence:** `screenshots/defects/D1_forgotten_password_message.png`
- **Note:** the test checks only "An email with a confirmation link has been sent", so it passes
  today and will keep passing after the wording is fixed.

## D-D1 – Empty wish list shows the shopping-cart message

- **Found by:** TC-D03 Wishlist, Scenarios 1 and 2 (`tests/D_cart_wishlist/test_wishlist.py`)
- **Severity:** Medium (misleading message on an account page)
- **Steps to reproduce:**
  1. Log in with an account whose wish list is empty (new account, or remove the last item).
  2. Open My Account > Wish List (`route=account/wishlist`).
- **Expected:** a heading "My Wish List" and a message that the wish list is empty.
- **Actual:** heading "Account" and the message "Your shopping cart is empty!"
- **Evidence:** `screenshots/defects/D-D1_empty_wish_list.png`

## E-D1 – Empty Order History shows the shopping-cart message

- **Found by:** TC-E03 Order History, Scenario 1 (`tests/E_checkout_orders/test_order_history.py`)
- **Severity:** Medium (misleading message on an account page)
- **Steps to reproduce:**
  1. Register a new account (it has no orders).
  2. Open My Account > Order History (`route=account/order`).
- **Expected:** a heading "Order History" and "You have not made any previous orders!"
- **Actual:** heading "Account" and the message "Your shopping cart is empty!"
  (the breadcrumb still correctly reads "Account > Order History")
- **Evidence:** `screenshots/defects/E-D1_empty_order_history.png`
- **Note:** the Order History and Order Information pages also show the heading "Account" when
  orders exist.

## E-D2 – Order details show an unfilled "#%s" placeholder

- **Found by:** the evidence screenshot of TC-E03 Order History, Scenario 3
  (`tests/E_checkout_orders/test_order_history.py`)
- **Severity:** Low (cosmetic; the real order number is still shown)
- **Steps to reproduce:**
  1. Log in and place an order (any product, Cash On Delivery).
  2. Open My Account > Order History (`route=account/order`) and click View on the order.
- **Expected:** "Order ID: #32944"
- **Actual:** "Order ID: #%s #32944": the "#%s" format placeholder is printed instead of being
  filled in
- **Evidence:** `screenshots/defects/E-D2_order_id_placeholder.png`
- **Note:** TC-E03 S3 checks the product, address, payment and shipping method, not the Order ID
  line, so it passes.

---

## Analysis

- **D-D1 and E-D1 most likely share one root cause.** Both empty-state pages show the generic
  heading "Account" and the shopping cart's empty text. In OpenCart these pages read their
  heading and empty-state text from per-page language entries (`heading_title`, `text_empty`), so
  the site's language files for the account pages are probably misconfigured or overridden.
  Fixing that one configuration would likely fix both defects; other empty account lists
  (e.g. Downloads, Returns, Reward Points) are worth checking for the same problem.
- **D1 and E-D2 are isolated text errors**: a missing word in the forgotten-password message, and
  a format placeholder in the order details that the page never fills in.
- **All four defects concern messages, not functionality.** Every main flow tested (register,
  log in, edit account, change password, address book, search, compare, cart, wish list,
  guest and registered checkout, order history) completed correctly.
