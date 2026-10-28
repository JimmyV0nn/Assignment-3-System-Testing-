# Defect Log

Defects found by the automated system tests on <https://opencart.abstracta.us/>.
Each defect is backed by a test that asserts the **correct** behaviour, so the test fails while
the defect exists and will pass once the site is fixed. Evidence screenshots are in
`screenshots/defects/`.

## Summary

| ID | Module | Test case / scenario | Severity | Summary | Status |
|---|---|---|---|---|---|
| D1 | A. Account Basics | TC-A03 Forgotten Password, S1 | Low | Success message is ungrammatical ("sent your email address") | Open |
| D-D1 | D. Shopping Cart & Wishlist | TC-D03 Wishlist, S1 and S2 | Medium | Empty wish list shows the shopping-cart message and heading "Account" | Open |
| E-D1 | E. Checkout & Orders | TC-E03 Order History, S1 | Medium | Empty Order History shows the shopping-cart message and heading "Account" | Open |

Severity scale: **High** – blocks a core task; **Medium** – the user is given wrong or misleading
information but can still complete the task; **Low** – cosmetic (wording, layout).

Expected full-suite result while these defects are open: **45 tests, 42 passed, 3 failed**
(TC-D03 S1, TC-D03 S2, TC-E03 S1). D1 does not fail its test, because TC-A03 S1 only checks the
opening phrase of the message.

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

---

## Analysis

- **D-D1 and E-D1 most likely share one root cause.** Both empty-state pages show the generic
  heading "Account" and the shopping cart's empty text. In OpenCart these pages read their
  heading and empty-state text from per-page language entries (`heading_title`, `text_empty`), so
  the site's language files for the account pages are probably misconfigured or overridden.
  Fixing that one configuration would likely fix both defects; other empty account lists
  (e.g. Downloads, Returns, Reward Points) are worth checking for the same problem.
- **D1 is an isolated wording error** in the forgotten-password success text.
- **All three defects concern messages, not functionality.** Every main flow tested (register,
  log in, edit account, change password, address book, search, compare, cart, wish list,
  guest and registered checkout, order history) completed correctly.
