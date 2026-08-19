USE olist_analysis;


-- ============================================================
-- FINAL DATA CLEANING
-- OLIST BUSINESS PERFORMANCE ANALYSIS
-- ============================================================
--
-- PURPOSE:
-- Create analysis-ready _clean tables from the raw Olist tables.
--
-- IMPORTANT:
-- 1. Raw tables are NOT modified.
-- 2. Legitimate NULL values are preserved.
-- 3. Missing business-event dates are NOT fabricated.
-- 4. Invalid values are handled according to the decisions
--    made during data investigation.
-- 5. We are NOT rebuilding the business analysis.
-- ============================================================


-- ============================================================
-- CLEANING DECISIONS
-- ============================================================
--
-- ORDERS
-- Keep legitimate NULL timestamps.
-- Remove rows missing essential identifiers/status.
--
-- CUSTOMERS
-- Remove rows missing customer identifiers.
-- Other missing attributes are preserved.
--
-- ORDER ITEMS
-- Remove rows missing essential identifiers.
-- Remove rows with negative price/freight because these are
-- invalid monetary values for the item-level analysis.
--
-- PAYMENTS
-- Keep the payment record but convert an invalid negative
-- payment value to NULL.
-- We do NOT invent a payment amount.
--
-- PRODUCTS
-- Keep the product.
-- Convert invalid/non-positive physical measurements to NULL
-- because the correct measurement is unknown.
--
-- MISSING PAYMENT ORDER:
-- bfbd0f9bdef84302105ad712db648a6c
--
-- The order is retained.
-- No payment is fabricated.
-- ============================================================



-- ============================================================
-- 1. CLEAN ORDERS
-- ============================================================

DROP TABLE IF EXISTS orders_clean;

CREATE TABLE orders_clean AS
SELECT
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date
FROM orders
WHERE order_id IS NOT NULL
  AND customer_id IS NOT NULL
  AND order_status IS NOT NULL;



-- ============================================================
-- 2. CLEAN CUSTOMERS
-- ============================================================

DROP TABLE IF EXISTS customers_clean;

CREATE TABLE customers_clean AS
SELECT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM customers
WHERE customer_id IS NOT NULL
  AND customer_unique_id IS NOT NULL;



-- ============================================================
-- 3. CLEAN ORDER ITEMS
-- ============================================================

DROP TABLE IF EXISTS order_items_clean;

CREATE TABLE order_items_clean AS
SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value
FROM order_items
WHERE order_id IS NOT NULL
  AND order_item_id IS NOT NULL
  AND product_id IS NOT NULL
  AND seller_id IS NOT NULL
  AND price >= 0
  AND freight_value >= 0;



-- ============================================================
-- 4. CLEAN PAYMENTS
-- ============================================================
--
-- Invalid negative payment values become NULL.
-- The payment record itself is retained.
-- ============================================================

DROP TABLE IF EXISTS payments_clean;

CREATE TABLE payments_clean AS
SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,

    CASE
        WHEN payment_value >= 0
        THEN payment_value
        ELSE NULL
    END AS payment_value

FROM payments
WHERE order_id IS NOT NULL;



-- ============================================================
-- 5. CLEAN PRODUCTS
-- ============================================================
--
-- Invalid/non-positive physical measurements become NULL.
-- The product itself is retained.
-- ============================================================

DROP TABLE IF EXISTS products_clean;

CREATE TABLE products_clean AS
SELECT
    product_id,
    product_category_name,

    CASE
        WHEN product_weight_g > 0
        THEN product_weight_g
        ELSE NULL
    END AS product_weight_g,

    CASE
        WHEN product_length_cm > 0
        THEN product_length_cm
        ELSE NULL
    END AS product_length_cm,

    CASE
        WHEN product_height_cm > 0
        THEN product_height_cm
        ELSE NULL
    END AS product_height_cm,

    CASE
        WHEN product_width_cm > 0
        THEN product_width_cm
        ELSE NULL
    END AS product_width_cm

FROM products
WHERE product_id IS NOT NULL;



-- ============================================================
-- 6. FINAL CLEANING VALIDATION
-- ============================================================


-- ------------------------------------------------------------
-- ORDERS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS clean_orders,
    COUNT(DISTINCT order_id) AS unique_order_ids,
    SUM(order_id IS NULL) AS order_id_nulls,
    SUM(customer_id IS NULL) AS customer_id_nulls,
    SUM(order_status IS NULL) AS status_nulls
FROM orders_clean;



-- ------------------------------------------------------------
-- CUSTOMERS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS clean_customer_rows,
    COUNT(DISTINCT customer_id) AS unique_customer_ids,
    COUNT(DISTINCT customer_unique_id) AS unique_customers,
    SUM(customer_id IS NULL) AS customer_id_nulls,
    SUM(customer_unique_id IS NULL) AS customer_unique_id_nulls
FROM customers_clean;



-- ------------------------------------------------------------
-- ORDER ITEMS
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS clean_order_items,
    SUM(price < 0) AS negative_prices,
    SUM(freight_value < 0) AS negative_freight,
    SUM(price IS NULL) AS price_nulls,
    SUM(freight_value IS NULL) AS freight_nulls
FROM order_items_clean;



-- ------------------------------------------------------------
-- PAYMENTS
-- ------------------------------------------------------------
--
-- The important check here is NULL payment values.
-- Negative values should now be zero.
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS clean_payment_rows,
    SUM(payment_value < 0) AS negative_payments,
    SUM(payment_value IS NULL) AS null_payment_values
FROM payments_clean;



-- ------------------------------------------------------------
-- PRODUCTS
-- ------------------------------------------------------------
--
-- Invalid measurements should now be NULL.
-- No non-positive values should remain.
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS clean_products,

    SUM(product_weight_g <= 0) AS invalid_weights,
    SUM(product_length_cm <= 0) AS invalid_lengths,
    SUM(product_height_cm <= 0) AS invalid_heights,
    SUM(product_width_cm <= 0) AS invalid_widths,

    SUM(product_weight_g IS NULL) AS null_weights,
    SUM(product_length_cm IS NULL) AS null_lengths,
    SUM(product_height_cm IS NULL) AS null_heights,
    SUM(product_width_cm IS NULL) AS null_widths

FROM products_clean;



-- ============================================================
-- 7. FINAL TABLE COUNTS
-- ============================================================

SELECT 'orders_clean' AS table_name, COUNT(*) AS row_count
FROM orders_clean

UNION ALL

SELECT 'customers_clean', COUNT(*)
FROM customers_clean

UNION ALL

SELECT 'order_items_clean', COUNT(*)
FROM order_items_clean

UNION ALL

SELECT 'payments_clean', COUNT(*)
FROM payments_clean

UNION ALL

SELECT 'products_clean', COUNT(*)
FROM products_clean;



-- ============================================================
-- 8. VERIFY THE KNOWN MISSING-PAYMENT ORDER
-- ============================================================
--
-- The order must remain in orders_clean.
-- We do not create a payment for it.
-- ============================================================

SELECT
    o.order_id,
    o.order_status,
    COUNT(oi.order_item_id) AS order_item_rows
FROM orders_clean o
LEFT JOIN order_items_clean oi
    ON o.order_id = oi.order_id
WHERE o.order_id = 'bfbd0f9bdef84302105ad712db648a6c'
GROUP BY
    o.order_id,
    o.order_status;



-- ============================================================
-- CLEANING COMPLETE
-- ============================================================
--
-- At this point:
--
-- RAW TABLES
--     orders
--     customers
--     order_items
--     payments
--     products
--
-- remain untouched.
--
-- CLEAN TABLES
--     orders_clean
--     customers_clean
--     order_items_clean
--     payments_clean
--     products_clean
--
-- are now ready for the BUSINESS ANALYSIS.
--
-- DO NOT continue modifying the cleaning logic unless a new
-- data-quality problem is discovered.
-- ============================================================