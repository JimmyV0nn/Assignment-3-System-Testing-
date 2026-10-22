# Shopping Cart & Wishlist (Module D)

Three test cases, each with three scenarios (9 scenarios in total). The tests are
self-contained: this folder ships its own `helpers.py` (page actions and checks) and
`conftest.py` (Chrome setup, throw-away wish list account, screenshot collection).

| Test case | Function | File |
|---|---|---|
| TC-D01 | Add to Cart | `test_add_to_cart.py` |
| TC-D02 | Update Shopping Cart | `test_update_cart.py` |
| TC-D03 | Wishlist | `test_wishlist.py` |

`test_cases.md` documents every scenario, its pass criteria and the recorded results
(9 PASS, 0 FAIL, 0 ERROR). Evidence screenshots are in `screenshots/D_cart_wishlist/`.

The three test functions use their own `helpers` import and the local fixtures
(`driver`, `shots`, `account`, `scenario`) defined by this folder's `conftest.py`, so
they run independently of the shared root conftest.
