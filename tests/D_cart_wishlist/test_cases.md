# Test Cases - D Module: Shopping Cart & Wishlist

**System under test:** OpenCart demo store - <https://opencart.abstracta.us/>
**Automation stack:** Python 3.12.9, Selenium 4.51.0, pytest 9.1.1, Google Chrome 155.0.8059.85
**Executed run:** `results/20261023-204621/` (2026-10-23 20:46:21 - 20:48:20, China Standard Time, UTC+0800, headless)
**Run result:** 9 of 9 scenarios PASS (total runtime 118 s)

**Common test data**

| Item | Value used by the tests |
| --- | --- |
| iPhone | product page `product_id=40`, Product Code `product 11`, unit price `$123.20` |
| iMac | product page `product_id=41`, Product Code `Product 14`, unit price `$122.00` |
| Wish list account | one throw-away account registered automatically before each wish list scenario (`dmodule.<random>@example.com`), credentials kept in memory only |

> Note on money: product line amounts are shown **tax inclusive**, while `Sub-Total` is **tax exclusive** and Eco Tax / VAT are listed separately for taxable products. The tests never assert `Sub-Total == sum of line totals`; they assert `Total == sum of line totals` and `Sub-Total + displayed taxes == Total`.

---

## D_TC01 - Add to Cart

**Function ID:** F4 Add to Cart
**Tester:** Yanyuan Liu (25745237)
**Code module:** `test_add_to_cart.py`

### D_TC01_S1 - Add a single product to an empty cart

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC01_S1 |
| **Function Name** | Add to Cart |
| **Scenario** | Add one iPhone to an empty shopping cart |
| **Precondition** | Fresh Chrome session; shopping cart is empty |
| **Steps** | 1. Open the shopping cart page; confirm the cart is empty.<br>2. Open `route=product/product&product_id=40` (iPhone).<br>3. Keep quantity = `1`.<br>4. Click **Add to Cart**.<br>5. Open the shopping cart page. |
| **Expected Result** | Product page shows iPhone / product 11 / `$123.20`; the confirmation "Success: You have added iPhone to your shopping cart!" is displayed; the cart contains exactly one line: iPhone, quantity 1, unit price `$123.20`, line total `$123.20`, and Total equals `$123.20`. |
| **Pass Criteria** | Cart empty before the action; product name/Product Code/price match the configured values; the add confirmation names the product; exactly 1 cart line with quantity 1 and correct amounts; Total equals the sum of line totals. |
| **Actual Result** | PASS (10.4 s). Cart went from empty to one iPhone line; Total `$123.20`. |
| **Status** | PASS |
| **Code** | `test_add_to_cart.py::test_add_single_item_to_empty_cart` |
| **Screenshots** | `D_TC01_S1_01_empty_cart_before.png`, `D_TC01_S1_04_cart_after_add.png` |

### D_TC01_S2 - Add the same product twice

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC01_S2 |
| **Function Name** | Add to Cart |
| **Scenario** | Click Add to Cart twice on the same iPhone page, quantity 1 each time |
| **Precondition** | Fresh Chrome session; shopping cart is empty |
| **Steps** | 1. Open the cart page and confirm it is empty.<br>2. Open the iPhone product page, quantity = `1`.<br>3. Click **Add to Cart**; wait for the confirmation and for the header cart badge to show `1`.<br>4. Click **Add to Cart** again; wait for the confirmation and for the badge to show `2`.<br>5. Open the shopping cart page. |
| **Expected Result** | Both clicks accepted; the cart holds one merged iPhone line with quantity `2`, unit price `$123.20`, line total `$246.40`, Total `$246.40`. |
| **Pass Criteria** | Each add confirmed (toast + badge) before the next click; exactly 1 line (not 2 duplicate lines); quantity = 2; line total = 2 × unit price; Total = sum of line totals. |
| **Actual Result** | PASS (12.0 s). One merged iPhone line, quantity 2, Total `$246.40`. |
| **Status** | PASS |
| **Code** | `test_add_to_cart.py::test_add_same_item_twice` |
| **Screenshots** | `D_TC01_S2_01_empty_cart_before.png`, `D_TC01_S2_05_cart_after_two_adds.png` |

### D_TC01_S3 - Add a different product

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC01_S3 |
| **Function Name** | Add to Cart |
| **Scenario** | Add iMac x1 to a cart that already contains iPhone x2 |
| **Precondition** | Fresh Chrome session; cart empty; iPhone x2 added through the product page |
| **Steps** | 1. Open the cart page and confirm it is empty.<br>2. Add iPhone twice (quantity 1 each click) and confirm the cart shows quantity 2.<br>3. Open the iMac product page (`product_id=41`) and verify name, Product Code and price.<br>4. Keep quantity = `1` and click **Add to Cart**.<br>5. Open the shopping cart page and read both lines and the totals block. |
| **Expected Result** | The cart contains two lines: iPhone x2 (`$246.40`) and iMac x1 (`$122.00`); the previous product keeps quantity 2; the totals block shows Sub-Total, taxes and Total exactly as displayed, with Total equal to the sum of the two line totals (`$368.40`). |
| **Pass Criteria** | iMac name/Product Code/price match the configured values; exactly 2 cart lines; iPhone quantity stays 2 with line total `$246.40`; iMac quantity 1 with line total `$122.00`; `Total == sum of line totals`; `Sub-Total + displayed taxes == Total`. |
| **Actual Result** | PASS (14.2 s). Cart showed iPhone x2 and iMac x1; Total `$368.40`. |
| **Status** | PASS |
| **Code** | `test_add_to_cart.py::test_add_different_product` |
| **Screenshots** | `D_TC01_S3_02_cart_with_iphone_two.png`, `D_TC01_S3_05_cart_with_two_products.png` |

---

## D_TC02 - Update Shopping Cart

**Function ID:** F5 Update Shopping Cart
**Tester:** Yanyuan Liu (25745237)
**Code module:** `test_update_cart.py`

### D_TC02_S1 - Increase the quantity

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC02_S1 |
| **Function Name** | Update Shopping Cart |
| **Scenario** | Change the iPhone quantity in the cart from 1 to 2 |
| **Precondition** | Fresh Chrome session; iPhone x1 in the cart |
| **Steps** | 1. Open the cart page and confirm one iPhone line with quantity `1`.<br>2. Change the quantity field to `2`.<br>3. Click the blue update (circular arrow) button.<br>4. Wait for the success message.<br>5. Reload the cart page from the server and read the stored values. |
| **Expected Result** | "Success: You have modified your shopping cart!" is displayed; after reload the quantity is `2`, line total `$246.40`, Total `$246.40`. |
| **Pass Criteria** | Success message contains "modified your shopping cart"; reloaded quantity = 2 (not just the typed value); line total = 2 × unit price; Total = sum of line totals. |
| **Actual Result** | PASS (11.5 s). Quantity 2 saved after reload, Total `$246.40`. |
| **Status** | PASS |
| **Code** | `test_update_cart.py::test_increase_quantity` |
| **Screenshots** | `D_TC02_S1_01_cart_before_update.png`, `D_TC02_S1_03_cart_after_update.png` |

### D_TC02_S2 - Decrease the quantity

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC02_S2 |
| **Function Name** | Update Shopping Cart |
| **Scenario** | Change the iPhone quantity in the cart from 2 to 1 |
| **Precondition** | Fresh Chrome session; iPhone x2 in the cart |
| **Steps** | 1. Open the cart page and confirm one iPhone line with quantity `2`.<br>2. Change the quantity field to `1`.<br>3. Click the update button.<br>4. Wait for the success message.<br>5. Reload the cart page and read the stored values. |
| **Expected Result** | "Success: You have modified your shopping cart!" is displayed; after reload the quantity is `1`, line total `$123.20`, Total `$123.20`. |
| **Pass Criteria** | Success message contains "modified your shopping cart"; reloaded quantity = 1; line total = unit price = `$123.20`; Total = sum of line totals. |
| **Actual Result** | PASS (13.6 s). Quantity 1 saved after reload, Total `$123.20`. |
| **Status** | PASS |
| **Code** | `test_update_cart.py::test_decrease_quantity` |
| **Screenshots** | `D_TC02_S2_01_cart_before_update.png`, `D_TC02_S2_03_cart_after_update.png` |

### D_TC02_S3 - Remove the product

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC02_S3 |
| **Function Name** | Update Shopping Cart |
| **Scenario** | Remove the only product from the cart |
| **Precondition** | Fresh Chrome session; cart contains only iPhone x1 |
| **Steps** | 1. Open the cart page and confirm exactly one iPhone line.<br>2. Click the red remove (x) button of that line.<br>3. Wait for the page to update and read the cart content. |
| **Expected Result** | The product line disappears and the cart shows "Your shopping cart is empty!". The site does not show a success banner for removing a product (observed behaviour), so only the empty-cart state is asserted. |
| **Pass Criteria** | No product rows remain in the cart table and the text "Your shopping cart is empty!" is present after the removal. |
| **Actual Result** | PASS (10.1 s). The line was removed and the cart showed "Your shopping cart is empty!". |
| **Status** | PASS |
| **Code** | `test_update_cart.py::test_remove_product` |
| **Screenshots** | `D_TC02_S3_01_cart_before_remove.png`, `D_TC02_S3_02_cart_after_remove.png` |

---

## D_TC03 - Wishlist

**Function ID:** F6 Wishlist
**Tester:** Yanyuan Liu (25745237)
**Code module:** `test_wishlist.py`
**Account note:** each scenario registers a throw-away account as preparation; no personal account is used. Registration is setup, not one of the three D test cases.

### D_TC03_S1 - Add a product to the wish list

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC03_S1 |
| **Function Name** | Wishlist |
| **Scenario** | Add iPhone to an empty wish list while logged in |
| **Precondition** | Logged in with a prepared test account; wish list is empty |
| **Steps** | 1. Log in with the test account.<br>2. Open My Wish List and confirm it is empty.<br>3. Open the iPhone product page (`product_id=40`) and verify the price.<br>4. Click the heart icon at the top right of the product image.<br>5. Open My Wish List. |
| **Expected Result** | "Success: You have added iPhone to your wish list!" is displayed; My Wish List shows one row: iPhone / product 11 / In Stock / `$123.20`. |
| **Pass Criteria** | Wish list empty before the action; the add confirmation names the product; exactly one wish list row with the correct name, Product Code, unit price `$123.20` and an "In Stock" stock status. |
| **Actual Result** | PASS (14.7 s). Wish list went from empty to one iPhone row showing "In Stock". |
| **Status** | PASS |
| **Code** | `test_wishlist.py::test_add_to_wishlist` |
| **Screenshots** | `D_TC03_S1_01_wishlist_empty_before.png`, `D_TC03_S1_04_wishlist_after_add.png` |

### D_TC03_S2 - Remove a product from the wish list

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC03_S2 |
| **Function Name** | Wishlist |
| **Scenario** | Delete the only product from My Wish List |
| **Precondition** | Logged in with a prepared test account; My Wish List contains exactly iPhone |
| **Steps** | 1. Log in and make sure the wish list contains only iPhone.<br>2. Open My Wish List.<br>3. Click the delete (x) button in the ACTION column of that row.<br>4. Read the page after it reloads. |
| **Expected Result** | "Success: You have modified your wish list!" is displayed, the product row is gone and the table shows the empty wish list state. |
| **Pass Criteria** | Success message contains "modified your wish list"; zero rows remain; the empty wish list message is displayed. |
| **Actual Result** | PASS (15.2 s). "Success: You have modified your wish list!" displayed; the row disappeared. |
| **Status** | PASS |
| **Code** | `test_wishlist.py::test_remove_from_wishlist` |
| **Screenshots** | `D_TC03_S2_01_wishlist_before_remove.png`, `D_TC03_S2_03_wishlist_after_remove.png` |

### D_TC03_S3 - Add a wish list item to the cart

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC03_S3 |
| **Function Name** | Wishlist |
| **Scenario** | Use the cart button in the wish list ACTION column to add iPhone to an empty cart |
| **Precondition** | Logged in with a prepared test account; My Wish List contains iPhone; shopping cart is empty |
| **Steps** | 1. Log in, clear the wish list, add iPhone to it.<br>2. Open the cart page and confirm it is empty.<br>3. Open My Wish List.<br>4. Click the cart button in the ACTION column once.<br>5. Open the shopping cart page. |
| **Expected Result** | "Success: You have added iPhone to your shopping cart!" is displayed; the cart contains iPhone x1 with unit price and line total `$123.20` and Total `$123.20`. The wish list entry is not required to disappear. |
| **Pass Criteria** | Add confirmation names the product; exactly one cart line with quantity 1 and correct amounts; Total = sum of line totals; the wish list state is only recorded, never asserted. |
| **Actual Result** | PASS (16.4 s). Cart had iPhone x1; the wish list still showed iPhone afterwards (recorded as information only). |
| **Status** | PASS |
| **Code** | `test_wishlist.py::test_wishlist_item_to_cart` |
| **Screenshots** | `D_TC03_S3_01_empty_cart_before.png`, `D_TC03_S3_04_cart_after_wishlist_add.png` |

---

## Run evidence

| Scenario | Status | Duration (s) | Test function |
| --- | --- | --- | --- |
| D_TC01_S1 | PASS | 10.4 | `test_add_to_cart.py::test_add_single_item_to_empty_cart` |
| D_TC01_S2 | PASS | 12.0 | `test_add_to_cart.py::test_add_same_item_twice` |
| D_TC01_S3 | PASS | 14.2 | `test_add_to_cart.py::test_add_different_product` |
| D_TC02_S1 | PASS | 11.5 | `test_update_cart.py::test_increase_quantity` |
| D_TC02_S2 | PASS | 13.6 | `test_update_cart.py::test_decrease_quantity` |
| D_TC02_S3 | PASS | 10.1 | `test_update_cart.py::test_remove_product` |
| D_TC03_S1 | PASS | 14.7 | `test_wishlist.py::test_add_to_wishlist` |
| D_TC03_S2 | PASS | 15.2 | `test_wishlist.py::test_remove_from_wishlist` |
| D_TC03_S3 | PASS | 16.4 | `test_wishlist.py::test_wishlist_item_to_cart` |
