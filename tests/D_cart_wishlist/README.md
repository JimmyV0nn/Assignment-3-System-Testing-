# Shopping Cart & Wishlist (Module D)

Three test cases, each with three scenarios (9 scenarios in total). The tests are
self-contained: this folder ships its own `helpers.py` (page actions and checks) and
`conftest.py` (Chrome setup, throw-away wish list account, screenshot collection).

| Test case | Function | File |
|---|---|---|
| TC-D01 | Add to Cart | `test_add_to_cart.py` |
| TC-D02 | Update Shopping Cart | `test_update_cart.py` |
| TC-D03 | Wishlist | `test_wishlist.py` |

`test_cases.md` documents every scenario, its pass criteria and the recorded results.
Evidence screenshots are in `screenshots/D_cart_wishlist/`.

The three test functions use their own `helpers` import and the local fixtures
(`driver`, `shots`, `account`, `scenario`) defined by this folder's `conftest.py`, so
they run independently of the shared root conftest.

## Running the D module

From the repository root, run only the D module with:

```bash
HEADLESS=1 pytest tests/D_cart_wishlist -v
```

Notes:

- The `--headless` flag is registered in this folder's own `conftest.py`, so it only
  works when you run pytest from inside `tests/D_cart_wishlist`. From the repository
  root use the `HEADLESS=1` environment variable instead (this always works).
- The site URL is **not** hard-coded in this module: `helpers.py` reads
  `common/config.py::BASE_URL`, so the site only needs to change in one place.
- Product names, Product Codes and prices are configured in `helpers.py` as expected
  values. If the demo site changes its prices the tests fail on purpose, so the
  configured expectations should be updated to match the site rather than copying the
  observed values into the assertions.
- Known defect: the empty wish list page shows "Your shopping cart is empty!" instead
  of a wish-list-empty message. The wish list scenarios assert the correct text, so
  `test_wishlist.py` fails while the site is defective (see `test_cases.md`).
