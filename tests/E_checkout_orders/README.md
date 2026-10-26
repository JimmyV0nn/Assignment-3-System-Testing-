# Checkout & Orders (Module E)

Three test cases, each with three scenarios (9 in total). They use the shared `driver` and
`registered_user` fixtures from the root `conftest.py`; checkout steps live in `checkout_steps.py`.

| Test case | Function | File |
|---|---|---|
| TC-E01 | Guest Checkout | `test_guest_checkout.py` |
| TC-E02 | Registered Checkout | `test_registered_checkout.py` |
| TC-E03 | Order History | `test_order_history.py` |

```bash
pytest tests/E_checkout_orders
```

Notes:

- Orders use **Cash On Delivery** and **Flat Shipping Rate**, so no payment details are entered.
- The checkout address is in Australia. Prices then show without UK VAT (e.g. iPhone $101.00 +
  $5.00 shipping), so the tests read totals from the page instead of hard-coding them.
- Scenarios that confirm an order place a real (test) order on the public demo store.
- **Known defect E-D1**: an empty Order History shows "Your shopping cart is empty!" (heading
  "Account") instead of "You have not made any previous orders!". `TC-E03` Scenario 1 asserts the
  correct text, so it fails on purpose while the site is defective (expected result: 8 pass, 1 fail).
