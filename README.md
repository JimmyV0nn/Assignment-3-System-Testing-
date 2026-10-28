# 32571 Assessment Task 3 – System Testing

Automated system tests for the [OpenCart demo store](https://opencart.abstracta.us/) (opencart.abstracta.us), written with **Python + Selenium + pytest**.

## Team & modules

| Module | Owner | Features under test | Folder |
|---|---|---|---|
| A. Account Basics | Tommy – Min Chia Huang (leader) | Registration, Login, Forgotten Password | `tests/A_account_basics` |
| B. Account Management | Jimmy – Jinhao Feng | Edit Account, Change Password, Address Book | `tests/B_account_management` |
| C. Product Discovery | Rathana Leng | Search, Category Filter, Product Compare | `tests/C_product_discovery` |
| D. Shopping Cart & Wishlist | Virg | Add to Cart, Update Shopping Cart, Wishlist | `tests/D_cart_wishlist` |
| E. Checkout & Orders | Jimmy – Jinhao Feng | Guest Checkout, Registered Checkout, Order History | `tests/E_checkout_orders` |

Each module has 3 test cases with 3 scenarios each (15 test cases, 45 scenarios in total).
Test case IDs follow `TC-<module letter><number>`, e.g. `TC-B01`.

## Project structure

```
conftest.py        # shared fixtures: driver, registered_user, auto screenshot on failure
common/config.py   # base URL, timeouts, url("route") helper
common/helpers.py  # register / login / logout, waits, take_screenshot
tests/<module>/    # each module's 3 test cases
screenshots/       # evidence screenshots saved during runs (not committed)
screenshots/defects/  # committed evidence for the defects in DEFECTS.md
DEFECTS.md         # defect log
```

## Setup

Requires Python 3.10+ and Google Chrome (Selenium Manager downloads ChromeDriver automatically).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Running tests

```bash
pytest                                   # everything
pytest tests/B_account_management        # one module
pytest --html=report.html                # with an HTML report
```

Set `HEADLESS=1` to run without opening a browser window.

## Expected results and defects

While the site's known defects are open, the full suite gives **45 tests: 42 passed, 3 failed**.
The 3 failures are intentional: each test asserts the correct behaviour and fails because of a
real defect on the site.

| ID | Failing scenario | Defect |
|---|---|---|
| D-D1 | TC-D03 S1, S2 | Empty wish list shows "Your shopping cart is empty!" |
| E-D1 | TC-E03 S1 | Empty Order History shows "Your shopping cart is empty!" |

Defect D1 (a wording error in the Forgotten Password message) is logged without failing a test.
Full details, reproduction steps and evidence are in [DEFECTS.md](DEFECTS.md).

## Conventions

- Use the `registered_user` fixture when a test needs a logged-in user. It registers a **new unique account** for every test, so nobody's test changes another member's data (e.g. passwords, addresses).
- Put reusable steps in `common/helpers.py` rather than copying them.
- Call `take_screenshot(driver, "TC-XNN_step")` at key steps for report evidence.
- Work on your own branch (`git checkout -b <your-name>`) and open a pull request into `main`.
