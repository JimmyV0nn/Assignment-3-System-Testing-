# Product Discovery (Module C)

Three test cases, each with three scenarios (9 in total). They use the shared `driver` fixture from
the root `conftest.py` and need no login.

| Test case | Function | File |
|---|---|---|
| TC-C01 | Product Search | `test_search.py` |
| TC-C02 | Category Navigation | `test_category_filter.py` |
| TC-C03 | Product Comparison | `test_product_comparison.py` |

```bash
pytest tests/C_product_discovery
```

Expected result: 9 passed.

Notes:

- TC-C02 opens categories from the top menu (Cameras, Components > Monitors, and the empty
  Software category) and checks the heading and the product listing of each.
- TC-C03 clears the browser cookies before each scenario so the comparison list starts empty.
