# 32571 Assessment Task 3 – System Testing

Automated system tests for the [LambdaTest eCommerce Playground](https://opencart.abstracta.us/), written with **Python + Selenium + pytest**.

## Team & modules

| Module | Owner | Features under test | Folder |
|---|---|---|---|
| A. Account Basics | Tommy (leader) | Registration, Login, Forgotten Password | `tests/A_account_basics` |
| B. Account Management | Jimmy | Edit Account, Change Password, Address Book | `tests/B_account_management` |
| C. Product Discovery | Rathana | Search, Category Filter, Product Compare | `tests/C_product_discovery` |
| D. Shopping Cart & Wishlist | Virg | Add to Cart, Update Shopping Cart, Wishlist | `tests/D_cart_wishlist` |
| E. Checkout & Orders | Jimmy | Guest Checkout, Registered Checkout, Order History | `tests/E_checkout_orders` |

Test case IDs follow `TC-<module letter><number>`, e.g. `TC-B01`.

## Project structure

```
conftest.py        # shared fixtures: driver, registered_user, auto screenshot on failure
common/config.py   # base URL, timeouts, url("route") helper
common/helpers.py  # register / login / logout, waits, take_screenshot
tests/<module>/    # each member's 3 test cases
screenshots/       # evidence screenshots saved during runs
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

## Conventions

- Use the `registered_user` fixture when a test needs a logged-in user. It registers a **new unique account** for every test, so nobody's test changes another member's data (e.g. passwords, addresses).
- Put reusable steps in `common/helpers.py` rather than copying them.
- Call `take_screenshot(driver, "TC-XNN_step")` at key steps for report evidence.
- Work on your own branch (`git checkout -b <your-name>`) and open a pull request into `main`.
