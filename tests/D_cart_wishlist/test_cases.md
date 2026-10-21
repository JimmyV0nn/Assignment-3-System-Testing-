# Test Cases - D Module: Shopping Cart & Wishlist

**System under test:** LambdaTest eCommerce Playground - <https://ecommerce-playground.lambdatest.io/index.php?route=common/home>
**Automation stack:** Python 3.12.9, Selenium 4.51.0, pytest 9.1.1, Google Chrome 155.0.8059.85
**Executed run:** `results/20261021-130707/` (2026-10-21 13:07:07 - 13:09:14, time zone China Standard Time, UTC+0800)
**Run result:** 9 of 9 scenarios PASS (total runtime 127 s)

**Common test data**
| Item | Value used by the tests |
| --- | --- |
| MacBook Pro | product page `product_id=45`, Product Code `Product 18`, unit price `$2,000.00` |
| iPhone | discovered via the search page for "iPhone" (product `40` in the recorded run), Product Code `product 11`, unit price `$123.20` |
| Wish list account | one throw-away account registered automatically before each wish list scenario (`dmodule.<random>@example.com`), credentials kept in memory only |

> Note on money: product line amounts are shown **tax inclusive**, while `Sub-Total` is **tax exclusive** and Eco Tax / VAT are listed separately. The tests never assert `Sub-Total == sum of line totals`; they assert `Total == sum of line totals` and `Sub-Total + displayed Eco Tax + displayed VAT == Total`.

---

## D_TC01 - Add to Cart

**Function ID:** [Confirm with group]
**Tester:** Yanyuan Liu (25745237)
**Code module:** `test_add_to_cart.py`

### D_TC01_S1 - Add a single product to an empty cart

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC01_S1 |
| **Function Name** | Add to Cart |
| **Scenario** | Add one MacBook Pro to an empty shopping cart |
| **Precondition** | Fresh Chrome session; shopping cart is empty |
| **Steps** | 1. Open the shopping cart page; confirm the cart is empty.<br>2. Open `route=product/product&product_id=45` (MacBook Pro).<br>3. Keep quantity = `1`.<br>4. Click **ADD TO CART**.<br>5. Open the shopping cart page. |
| **Expected Result** | 1. Cart page shows "Your shopping cart is empty!".<br>2. Product page shows MacBook Pro / Product 18 / `$2,000.00`.<br>3. A success confirmation "Success: You have added MacBook Pro to your shopping cart!" is displayed.<br>4. Cart contains exactly one product line: MacBook Pro, quantity 1, unit price `$2,000.00`, line total `$2,000.00`, and the cart Total equals `$2,000.00`. |
| **Pass Criteria** | All of the following: cart was empty before the action; product name, Product Code and price on the product page equal the configured values; the add confirmation names the product; the cart has exactly 1 line with the same name/model, quantity 1, unit price and line total `$2,000.00`; page Total `$2,000.00` and Total = sum of line totals. |
| **Actual Result** | Cart was empty. Product page showed MacBook Pro / Product 18 / `$2,000.00`. Toast: "Success: You have added MacBook Pro to your shopping cart!". Cart page: 1 line, MacBook Pro, Product 18, quantity 1, unit price `$2,000.00`, line total `$2,000.00`, Total `$2,000.00` (no separate tax line displayed for this single-item cart). |
| **Status** | PASS (10.7 s) |
| **Code** | `test_add_to_cart.py::test_add_single_item_to_empty_cart` |
| **Screenshots** | `results/20261021-130707/screenshots/D_TC01_S1_01_empty_cart_before.png`, `..._02_product_page_before_add.png`, `..._03_add_to_cart_confirmation.png`, `..._04_cart_after_add.png` |

### D_TC01_S2 - Add the same product twice

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC01_S2 |
| **Function Name** | Add to Cart |
| **Scenario** | Click ADD TO CART twice on the same product page, quantity 1 each time |
| **Precondition** | Fresh Chrome session; shopping cart is empty |
| **Steps** | 1. Open the cart page and confirm it is empty.<br>2. Open the MacBook Pro product page, quantity = `1`.<br>3. Click **ADD TO CART**; wait for the confirmation of this add and for the header cart badge to show `1`.<br>4. Without changing the quantity, click **ADD TO CART** again; wait for the confirmation of this add and for the badge to show `2`.<br>5. Open the shopping cart page. |
| **Expected Result** | Both clicks are accepted; the cart holds a single merged MacBook Pro line with quantity `2`, unit price `$2,000.00`, line total `$4,000.00`, and Total `$4,000.00`. |
| **Pass Criteria** | Each add is confirmed on the page (toast + cart badge) before the next click; the cart contains exactly 1 line (not 2 duplicate lines); quantity = 2; line total = `$4,000.00` = 2 × unit price; Total = sum of line totals = `$4,000.00`. |
| **Actual Result** | Both adds confirmed (badge 1 then 2, two success toasts). Cart showed one MacBook Pro line, quantity `2`, unit price `$2,000.00`, line total `$4,000.00`, Total `$4,000.00`. |
| **Status** | PASS (11.7 s) |
| **Code** | `test_add_to_cart.py::test_add_same_item_twice` |
| **Screenshots** | `.../D_TC01_S2_01_empty_cart_before.png`, `..._02_product_page_quantity_1.png`, `..._03_first_add_confirmed.png`, `..._04_second_add_confirmed.png`, `..._05_cart_after_two_adds.png` |

### D_TC01_S3 - Add a different product

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC01_S3 |
| **Function Name** | Add to Cart |
| **Scenario** | Add iPhone x1 to a cart that already contains MacBook Pro x2 |
| **Precondition** | Fresh Chrome session; cart empty; MacBook Pro x2 added through the product page |
| **Steps** | 1. Open the cart page and confirm it is empty.<br>2. Add MacBook Pro twice (quantity 1 each click) and confirm the cart shows quantity 2.<br>3. Search "iPhone" on the site and open the first result named exactly "iPhone" (do not guess the product id).<br>4. Verify the iPhone page shows Product Code `product 11` and unit price `$123.20`.<br>5. Keep quantity = `1` and click **ADD TO CART**.<br>6. Open the shopping cart page and read both lines and the totals block. |
| **Expected Result** | The cart contains two different lines: MacBook Pro x2 (`$4,000.00`) and iPhone x1 (`$123.20`). The previous product keeps quantity 2. The totals block shows Sub-Total, Eco Tax, VAT and Total exactly as displayed by the site, with Total equal to the sum of the two line totals (`$4,123.20`). |
| **Pass Criteria** | iPhone is located through search results and its name / Product Code / price match the configured values; exactly 2 cart lines; MacBook Pro quantity stays 2 with line total `$4,000.00`; iPhone quantity 1 with line total `$123.20`; `Total == sum of line totals`; `Sub-Total + Eco Tax + VAT == Total`. |
| **Actual Result** | iPhone located via search (product 40), Product Code `product 11`, `$123.20`, added successfully. Cart: MacBook Pro quantity 2 line total `$4,000.00`; iPhone quantity 1 line total `$123.20`; Sub-Total `$4,101.00`, Eco Tax `$2.00`, VAT `$20.20`, Total `$4,123.20` (`4,101.00 + 2.00 + 20.20 = 4,123.20`, and `4,000.00 + 123.20 = 4,123.20`). This matches the manual observation supplied with the assignment. |
| **Status** | PASS (17.4 s) |
| **Code** | `test_add_to_cart.py::test_add_different_product` |
| **Screenshots** | `.../D_TC01_S3_01_empty_cart_before.png`, `..._02_cart_with_macbook_two.png`, `..._03_iphone_product_page.png`, `..._04_iphone_add_confirmed.png`, `..._05_cart_with_two_products.png` |

---

## D_TC02 - Update Shopping Cart

**Function ID:** [Confirm with group]
**Tester:** Yanyuan Liu (25745237)
**Code module:** `test_update_cart.py`

### D_TC02_S1 - Increase the quantity

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC02_S1 |
| **Function Name** | Update Shopping Cart |
| **Scenario** | Change the MacBook Pro quantity in the cart from 1 to 2 |
| **Precondition** | Fresh Chrome session; MacBook Pro x1 in the cart |
| **Steps** | 1. Open the cart page and confirm one MacBook Pro line with quantity `1`.<br>2. Change the quantity field to `2`.<br>3. Click the blue update (circular arrow) button.<br>4. Wait for the success message.<br>5. Reload the cart page from the server and read the stored values. |
| **Expected Result** | "Success: You have modified your shopping cart!" is displayed; after reload the quantity is `2`, unit price `$2,000.00`, line total `$4,000.00`, Total `$4,000.00`. |
| **Pass Criteria** | Success message contains "modified your shopping cart"; the value read **after reload** is 2 (not just the typed value); line total = 2 × unit price; Total = sum of line totals. |
| **Actual Result** | Success message displayed. After reload: quantity `2`, unit price `$2,000.00`, line total `$4,000.00`, Total `$4,000.00`. |
| **Status** | PASS (11.0 s) |
| **Code** | `test_update_cart.py::test_increase_quantity` |
| **Screenshots** | `.../D_TC02_S1_01_cart_before_update.png`, `..._02_update_success_message.png`, `..._03_cart_after_update.png` |

### D_TC02_S2 - Decrease the quantity

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC02_S2 |
| **Function Name** | Update Shopping Cart |
| **Scenario** | Change the MacBook Pro quantity in the cart from 2 to 1 |
| **Precondition** | Fresh Chrome session; MacBook Pro x2 in the cart |
| **Steps** | 1. Open the cart page and confirm one MacBook Pro line with quantity `2`.<br>2. Change the quantity field to `1`.<br>3. Click the update button.<br>4. Wait for the success message.<br>5. Reload the cart page and read the stored values. |
| **Expected Result** | "Success: You have modified your shopping cart!" is displayed; after reload the quantity is `1`, line total `$2,000.00`, Total `$2,000.00`. |
| **Pass Criteria** | Success message contains "modified your shopping cart"; reloaded quantity = 1; line total = unit price = `$2,000.00`; Total = sum of line totals. |
| **Actual Result** | Success message displayed. After reload: quantity `1`, line total `$2,000.00`, Total `$2,000.00`. |
| **Status** | PASS (14.4 s) |
| **Code** | `test_update_cart.py::test_decrease_quantity` |
| **Screenshots** | `.../D_TC02_S2_01_cart_before_update.png`, `..._02_update_success_message.png`, `..._03_cart_after_update.png` |

### D_TC02_S3 - Remove the product

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC02_S3 |
| **Function Name** | Update Shopping Cart |
| **Scenario** | Remove the only product from the cart |
| **Precondition** | Fresh Chrome session; cart contains only MacBook Pro x1 |
| **Steps** | 1. Open the cart page and confirm exactly one MacBook Pro line.<br>2. Click the red remove (x) button of that line.<br>3. Wait for the page to update and read the cart content. |
| **Expected Result** | The product line disappears and the cart shows "Your shopping cart is empty!". |
| **Pass Criteria** | No product rows remain in the cart table and the text "Your shopping cart is empty!" is present after the removal. |
| **Actual Result** | The line was removed and the cart showed "Your shopping cart is empty!". The site does **not** display a success banner for removing a product (observed behaviour, so no banner assertion was made - only the empty-cart state is asserted). |
| **Status** | PASS (10.6 s) |
| **Code** | `test_update_cart.py::test_remove_product` |
| **Screenshots** | `.../D_TC02_S3_01_cart_before_remove.png`, `..._02_cart_after_remove.png` |

---

## D_TC03 - Wishlist

**Function ID:** [Confirm with group]
**Tester:** Yanyuan Liu (25745237)
**Code module:** `test_wishlist.py`
**Account note:** each scenario registers a throw-away account as preparation; no personal account is used. Registration is setup, not one of the three D test cases.

### D_TC03_S1 - Add a product to the wish list

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC03_S1 |
| **Function Name** | Wishlist |
| **Scenario** | Add MacBook Pro to an empty wish list while logged in |
| **Precondition** | Logged in with a prepared test account; wish list is empty |
| **Steps** | 1. Log in with the test account.<br>2. Open My Wish List and confirm it is empty ("No results!").<br>3. Open the MacBook Pro product page (`product_id=45`) and verify the price.<br>4. Click the heart icon at the top right of the product image.<br>5. Open My Wish List. |
| **Expected Result** | "Success: You have added MacBook Pro to your wish list!" is displayed; My Wish List shows one row: MacBook Pro / Product 18 / In Stock / `$2,000.00`. |
| **Pass Criteria** | Wish list was empty before the action; the add confirmation names the product; exactly one wish list row with the correct name, Product Code, unit price `$2,000.00` and an "In Stock" stock status. |
| **Actual Result** | Wish list was empty ("No results!"). Heart click produced "Success: You have added MacBook Pro to your wish list! Wish List (1)". My Wish List showed MacBook Pro / Product 18 / In Stock / `$2,000.00`. |
| **Status** | PASS (15.8 s) |
| **Code** | `test_wishlist.py::test_add_to_wishlist` |
| **Screenshots** | `.../D_TC03_S1_01_wishlist_empty_before.png`, `..._02_product_page_before_wishlist.png`, `..._03_wishlist_confirmation.png`, `..._04_wishlist_after_add.png` |

### D_TC03_S2 - Remove a product from the wish list

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC03_S2 |
| **Function Name** | Wishlist |
| **Scenario** | Delete the only product from My Wish List |
| **Precondition** | Logged in with a prepared test account; My Wish List contains exactly MacBook Pro |
| **Steps** | 1. Log in and make sure the wish list contains only MacBook Pro.<br>2. Open My Wish List.<br>3. Click the delete (x) button in the ACTION column of that row.<br>4. Read the page after it reloads. |
| **Expected Result** | "Success: You have modified your wish list!" is displayed, the product row is gone and the table shows "No results!". |
| **Pass Criteria** | Success message contains "modified your wish list"; zero rows remain; the text "No results!" is displayed. |
| **Actual Result** | "Success: You have modified your wish list!" displayed; the row disappeared and the page showed "No results!". |
| **Status** | PASS (15.4 s) |
| **Code** | `test_wishlist.py::test_remove_from_wishlist` |
| **Screenshots** | `.../D_TC03_S2_01_wishlist_before_remove.png`, `..._02_remove_success_message.png`, `..._03_wishlist_after_remove.png` |

### D_TC03_S3 - Add a wish list item to the cart

| Field | Content |
| --- | --- |
| **Test Case ID** | D_TC03_S3 |
| **Function Name** | Wishlist |
| **Scenario** | Use the cart button in the wish list ACTION column to add MacBook Pro to an empty cart |
| **Precondition** | Logged in with a prepared test account; My Wish List contains MacBook Pro; shopping cart is empty |
| **Steps** | 1. Log in, clear the wish list, add MacBook Pro to it.<br>2. Open the cart page and confirm it is empty.<br>3. Open My Wish List.<br>4. Click the cart button in the ACTION column once.<br>5. Open the shopping cart page. |
| **Expected Result** | "Success: You have added MacBook Pro to your shopping cart!" is displayed; the cart contains MacBook Pro x1 with unit price and line total `$2,000.00` and Total `$2,000.00`. The wish list entry is **not** required to disappear. |
| **Pass Criteria** | Add confirmation names the product; exactly one cart line with quantity 1 and correct amounts; Total = sum of line totals; the wish list state is only recorded, never asserted. |
| **Actual Result** | Toast "Success: You have added MacBook Pro to your shopping cart!". Cart: MacBook Pro x1, unit price `$2,000.00`, line total `$2,000.00`, Total `$2,000.00`. The wish list still shows MacBook Pro afterwards (recorded as information only). |
| **Status** | PASS (20.1 s) |
| **Code** | `test_wishlist.py::test_wishlist_item_to_cart` |
| **Screenshots** | `.../D_TC03_S3_01_empty_cart_before.png`, `..._02_wishlist_before_add_to_cart.png`, `..._03_add_to_cart_confirmation.png`, `..._04_cart_after_wishlist_add.png` |

---

## Run evidence

| Scenario | Status | Duration (s) | Test function |
| --- | --- | --- | --- |
| D_TC01_S1 | PASS | 10.7 | `test_add_to_cart.py::test_add_single_item_to_empty_cart` |
| D_TC01_S2 | PASS | 11.7 | `test_add_to_cart.py::test_add_same_item_twice` |
| D_TC01_S3 | PASS | 17.4 | `test_add_to_cart.py::test_add_different_product` |
| D_TC02_S1 | PASS | 11.0 | `test_update_cart.py::test_increase_quantity` |
| D_TC02_S2 | PASS | 14.4 | `test_update_cart.py::test_decrease_quantity` |
| D_TC02_S3 | PASS | 10.6 | `test_update_cart.py::test_remove_product` |
| D_TC03_S1 | PASS | 15.8 | `test_wishlist.py::test_add_to_wishlist` |
| D_TC03_S2 | PASS | 15.4 | `test_wishlist.py::test_remove_from_wishlist` |
| D_TC03_S3 | PASS | 20.1 | `test_wishlist.py::test_wishlist_item_to_cart` |

Executed on 2026-10-21 (UTC+0800) with Chrome 155.0.8059.85 in visible (non-headless) mode, so the run can be observed;
`screenshots/` contains 33 screenshots from this run, and `run.log` / `summary.md` / `results.csv` hold the raw outcome of every scenario. All values above are copied from these real run artifacts.
