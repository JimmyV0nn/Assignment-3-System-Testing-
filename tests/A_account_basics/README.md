# Account Basics (Module A)

Owner: Min Chia Huang (26157901). Three test cases, each with three scenarios (9 in total). They
use the shared `driver` and `registered_user` fixtures from the root `conftest.py` and the
register / login / logout helpers in `common/helpers.py`.

| Test case | Report ID | Function | File |
|---|---|---|---|
| TC-A01 | T001 | User Registration | `test_registration.py` |
| TC-A02 | T002 | User Login | `test_login.py` |
| TC-A03 | T003 | Forgotten Password | `test_forgotten_password.py` |

| Test case | Scenario 1 | Scenario 2 | Scenario 3 |
|---|---|---|---|
| TC-A01 Registration | valid details → `account/success` | email already registered → warning | 3-character password (boundary, allowed 4-20) → field error |
| TC-A02 Login | valid credentials → `account/account`, "My Account" | wrong password → no-match warning | empty fields → no-match warning |
| TC-A03 Forgotten Password | registered email → back to login with success message | unregistered email → not-found warning | empty email → warning, no success message |

```bash
pytest tests/A_account_basics
```

Expected result: 9 passed.

Notes:

- Every scenario that needs an existing account gets a fresh one from the `registered_user`
  fixture (a random `@example.com` address) and logs out first, so no scenario depends on another.
- Each test saves a screenshot of the result page in `screenshots/`. The page screenshot has no
  address bar, so the tests assert the URL route as well as the message text.
- **Known defect A-D1**: the password reset success message is missing the word "to" ("...has
  been sent your email address."). TC-A03 Scenario 1 checks only the start of the message, so it
  still passes; the defect is recorded in the report.
