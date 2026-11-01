# 32571 Software Testing – Assessment Task 3: System Testing

Automated system tests for the [OpenCart demo store](https://opencart.abstracta.us/), an
e-commerce site where customers search for products, manage a cart and a wish list, and place
orders as a guest or as a registered customer.

- **Subject:** 32571 Software Testing, UTS · Tutorial group 32571_Tou1/02
- **System under test:** <https://opencart.abstracta.us/> (OpenCart 2.x, default theme)
- **Tools:** Python 3.10+, Selenium WebDriver 4, pytest 8, Google Chrome
- **Scope:** 15 functions in 5 modules · 15 test cases · 45 scenarios · 4 defects found

## Team

| Member | Role | Module | Report sections |
|---|---|---|---|
| Min Chia Huang (Tommy) | Team leader, tester | A. Account Basics | 3 Test Team, final integration and submission |
| Jinhao Feng (Jimmy) | Tester, repository maintainer | B. Account Management, E. Checkout & Orders | 2 System Functions and dependency graph |
| Rathana Leng | Tester | C. Product Discovery | 1 Overview, 5 Test Environments and Tools |
| Yanyuan Liu (Virgil) | Tester | D. Shopping Cart & Wishlist | 4 Task Schedule |

## Functions and test cases

Every function has one test case with three scenarios: usually one valid case and two invalid
or boundary inputs. Test IDs in the code (`TC-…`) map to the IDs used in the report (`T0…`).

| Function | Module | Test case | Report ID | File | Owner |
|---|---|---|---|---|---|
| F1 User Login | A | TC-A02 | T002 | `tests/A_account_basics/test_login.py` | Min Chia Huang |
| F2 User Registration | A | TC-A01 | T001 | `tests/A_account_basics/test_registration.py` | Min Chia Huang |
| F3 Forgotten Password | A | TC-A03 | T003 | `tests/A_account_basics/test_forgotten_password.py` | Min Chia Huang |
| F4 Add to Cart | D | TC-D01 | T004 | `tests/D_cart_wishlist/test_add_to_cart.py` | Yanyuan Liu |
| F5 Update Shopping Cart | D | TC-D02 | T005 | `tests/D_cart_wishlist/test_update_cart.py` | Yanyuan Liu |
| F6 Wishlist | D | TC-D03 | T006 | `tests/D_cart_wishlist/test_wishlist.py` | Yanyuan Liu |
| F7 Edit Account | B | TC-B01 | T007 | `tests/B_account_management/test_edit_account.py` | Jinhao Feng |
| F8 Change Password | B | TC-B02 | T008 | `tests/B_account_management/test_change_password.py` | Jinhao Feng |
| F9 Address Book | B | TC-B03 | T009 | `tests/B_account_management/test_address_book.py` | Jinhao Feng |
| F10 Product Search | C | TC-C01 | T010 | `tests/C_product_discovery/test_search.py` | Rathana Leng |
| F11 Category Filter | C | TC-C02 | T011 | `tests/C_product_discovery/test_category_filter.py` | Rathana Leng |
| F12 Product Compare | C | TC-C03 | T012 | `tests/C_product_discovery/test_product_comparison.py` | Rathana Leng |
| F13 Guest Checkout | E | TC-E01 | T013 | `tests/E_checkout_orders/test_guest_checkout.py` | Jinhao Feng |
| F14 Registered Checkout | E | TC-E02 | T014 | `tests/E_checkout_orders/test_registered_checkout.py` | Jinhao Feng |
| F15 Order History | E | TC-E03 | T015 | `tests/E_checkout_orders/test_order_history.py` | Jinhao Feng |

Each module folder has its own README with scenario details.

### Dependencies

F2 User Registration, F1 User Login and F4 Add to Cart are tested first: 9 of the other 12
functions need at least one of them.

- F1 and F3 need an account (F2).
- F6, F7, F8, F9, F14 and F15 need a logged-in customer (F1).
- F5, F13 and F14 need a non-empty cart (F4).
- F15 needs an order placed through F14 before it can list one.
- F10, F11 and F12 have no dependencies on other modules.

## Project structure

```
conftest.py                    shared fixtures: driver (Chrome), registered_user, screenshot on failure
pytest.ini                     test path, verbose output, JUnit XML results in reports/junit.xml
requirements.txt               selenium, pytest, pytest-html
common/
  config.py                    BASE_URL, timeouts, HEADLESS switch, url("route") helper
  helpers.py                   register / login / logout, waits, form filling, take_screenshot
tests/
  A_account_basics/            3 test files
  B_account_management/        3 test files
  C_product_discovery/         3 test files
  D_cart_wishlist/             3 test files + own conftest.py, helpers.py and test_cases.md
  E_checkout_orders/           3 test files + checkout_steps.py (cart and 6-step checkout)
DEFECTS.md                     defect log with reproduction steps and evidence
screenshots/                   evidence saved during runs (not committed)
screenshots/defects/           committed evidence for each defect in DEFECTS.md
screenshots/D_cart_wishlist/   committed evidence for Module D
reports/                       JUnit XML results (not committed)
```

## Setup

You need Python 3.10 or later and Google Chrome. Selenium Manager downloads the matching
ChromeDriver automatically on the first run.

**Windows (PowerShell)**

```powershell
git clone https://github.com/JimmyV0nn/Assignment-3-System-Testing-.git
cd Assignment-3-System-Testing-
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activation fails with "running scripts is disabled", run
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and activate again.

**macOS / Linux**

```bash
git clone https://github.com/JimmyV0nn/Assignment-3-System-Testing-.git
cd Assignment-3-System-Testing-
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Activate the virtual environment in every new terminal before running `pytest`.

## Running tests

| What | Command |
|---|---|
| Everything (45 scenarios) | `pytest` |
| One module | `pytest tests/B_account_management` |
| One test case | `pytest tests/E_checkout_orders/test_guest_checkout.py` |
| One scenario | `pytest tests/E_checkout_orders/test_guest_checkout.py::test_s1_guest_completes_order` |
| Scenarios matching a keyword | `pytest tests/B_account_management -k password` |
| Stop at the first failure | `pytest -x` |
| HTML report | `pytest --html=report.html` |

**Without a browser window (headless):**

```powershell
$env:HEADLESS="1"; pytest          # Windows PowerShell
```

```bash
HEADLESS=1 pytest                  # macOS / Linux
```

A full run takes about 8–10 minutes with a visible browser. Every run also writes JUnit XML
results to `reports/junit.xml`.

## Test data and side effects

- Tests that need a customer register a **new account** each time
  (`tester.<10 random hex characters>@example.com`, password `Test@12345`), so no test changes
  another test's data. Module D uses its own throw-away accounts (`dmodule.<random>@example.com`).
- Checkout tests use an Australian address (15 Broadway, Ultimo NSW 2007), **Flat Shipping
  Rate** and **Cash On Delivery**, so no payment details are ever entered. With an Australian
  address the site shows prices without UK tax (iPhone $101.00 + $5.00 shipping).
- Running the suite creates real accounts and test orders on the public demo store.

## Evidence

- Tests save screenshots at key steps to `screenshots/`, named `<test ID>_<step>_<timestamp>.png`
  (for example `TC-B02_S1_success_20261028-201211.png`).
- When a test fails, the browser is captured automatically as `FAILED_<test name>_<timestamp>.png`.
- Module D writes a full run summary (screenshots, log, CSV, Markdown) to
  `tests/D_cart_wishlist/results/<run time>/`.

## Expected results

The suite is designed so that a test **fails while a real defect exists** and passes once the
site is fixed. With the current site the full run gives **45 tests: 42 passed, 3 failed**.

| Module | Owner | Scenarios | Passed | Failed | Notes |
|---|---|---|---|---|---|
| A. Account Basics | Min Chia Huang | 9 | 9 | 0 | |
| B. Account Management | Jinhao Feng | 9 | 9 | 0 | |
| C. Product Discovery | Rathana Leng | 9 | 9 | 0 | |
| D. Shopping Cart & Wishlist | Yanyuan Liu | 9 | 7 | 2 | TC-D03 S1, S2 fail on purpose (D-D1) |
| E. Checkout & Orders | Jinhao Feng | 9 | 8 | 1 | TC-E03 S1 fails on purpose (E-D1) |
| **Total** | | **45** | **42** | **3** | |

## Defects found

| ID | Severity | Found by | Defect |
|---|---|---|---|
| D1 | Low | TC-A03 S1 | Forgotten Password message reads "has been sent your email address" ("to" is missing) |
| D-D1 | Medium | TC-D03 S1, S2 | Empty wish list shows the heading "Account" and "Your shopping cart is empty!" |
| E-D1 | Medium | TC-E03 S1 | Empty Order History shows the heading "Account" and "Your shopping cart is empty!" |
| E-D2 | Low | TC-E03 S3 (screenshot) | Order details show "Order ID: #%s #32944": an unfilled format placeholder |

D1 and E-D2 do not fail a test: TC-A03 checks only the start of the message, and TC-E03 S3 does
not check the Order ID line. Reproduction steps, evidence and analysis are in
[DEFECTS.md](DEFECTS.md).

## Working on the repository

- Create a branch for your work (`git switch -c feature/<your-name>-<topic>`), push it, and
  open a pull request into `main`. Ask another member to review and approve it before merging.
- Name tests and screenshots with the test ID (`TC-<module letter><number>`, e.g. `TC-B01`) and
  the scenario (`S1`–`S3`).
- Use the `registered_user` fixture when a test needs a logged-in customer, and put steps that
  more than one test needs in `common/helpers.py` (or the module's own helper file).
- On pages that load content in the background (the checkout, region lists), wait for the
  loading to finish before the next click. `checkout_steps.py` shows how (`wait_ajax_idle`).

## Troubleshooting

| Problem | Fix |
|---|---|
| `pytest` is not recognized | The virtual environment is not active: run `.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` |
| `--headless` is rejected | That flag only exists inside `tests/D_cart_wishlist`; use the `HEADLESS=1` environment variable instead |
| A checkout test fails with "Payment method required!" | A click happened before the page finished loading; run it again and report it if it repeats |
| Many tests time out | The demo site is slow or down; open <https://opencart.abstracta.us/> in a browser and try again later |
