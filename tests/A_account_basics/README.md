# Account Basics (Module A)

Three test cases, each with three scenarios (9 in total). They use the shared `driver` and
`registered_user` fixtures from the root `conftest.py` and the register / login / logout helpers
in `common/helpers.py`.

| Test case | Function | File |
|---|---|---|
| TC-A01 | User Registration | `test_registration.py` |
| TC-A02 | User Login | `test_login.py` |
| TC-A03 | Forgotten Password | `test_forgotten_password.py` |

```bash
pytest tests/A_account_basics
```

Expected result: 9 passed.

Notes:

- Scenarios that need an existing account get a fresh one from `registered_user` and log out
  first, so no scenario depends on another.
- TC-A01 Scenario 3 is a boundary value test: a 3-character password, where the allowed range
  is 4-20.
- Known defect A-D1: the password reset message reads "has been sent your email address" (the
  word "to" is missing). TC-A03 Scenario 1 checks only the start of the message, so it passes.
