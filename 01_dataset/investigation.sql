CREATE DATABASE olist_analysis;
USE olist_analysis;
CREATE DATABASE IF NOT EXISTS olist_analysis;
USE olist_analysis;


-- ============================================================
-- PART 1: RAW DATA VALIDATION
-- IMPORTANT:
-- We DO NOT modify the original tables.
-- ============================================================

-- ============================================================
-- 1. ORDERS - BASIC VALIDATION
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_order_ids,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_ids
FROM orders;


SELECT
    SUM(order_id IS NULL) AS order_id_nulls,
    SUM(customer_id IS NULL) AS customer_id_nulls,
    SUM(order_status IS NULL) AS order_status_nulls,
    SUM(order_purchase_timestamp IS NULL) AS purchase_timestamp_nulls,
    SUM(order_approved_at IS NULL) AS approved_timestamp_nulls,
    SUM(order_delivered_carrier_date IS NULL) AS carrier_timestamp_nulls,
    SUM(order_delivered_customer_date IS NULL) AS delivered_timestamp_nulls,
    SUM(order_estimated_delivery_date IS NULL) AS estimated_delivery_nulls
FROM orders;

SELECT
    order_status,
    COUNT(*) AS total_orders,
    SUM(order_approved_at IS NULL) AS approved_nulls,
    SUM(order_delivered_carrier_date IS NULL) AS carrier_nulls,
    SUM(order_delivered_customer_date IS NULL) AS delivered_nulls
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- HOW MANY DATES ORDER DELIVERD LATE
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
WHERE order_status = 'delivered'
  AND (
      order_approved_at IS NULL
      
      and  order_delivered_customer_date IS NULL
  );
  
  
-- ============================================================
-- 2. CUSTOMERS - BASIC VALIDATION
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS customer_ids,
	COUNT(DISTINCT customer_unique_id) AS unique_customer_ids
FROM customers;



SELECT
    SUM(customer_id IS NULL) AS customer_id_nulls,
    SUM(customer_unique_id IS NULL) AS customer_unique_id_nulls,
    SUM(customer_zip_code_prefix IS NULL) AS zip_nulls,
    SUM(customer_city IS NULL) AS city_nulls,
    SUM(customer_state IS NULL) AS state_nulls
FROM customers;


SELECT
    COUNT(*) AS total_customer_rows,
    COUNT(DISTINCT customer_unique_id) AS actual_unique_customers
FROM customers;


-- ============================================================
-- 3. ORDER ITEMS - BASIC VALIDATION
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT product_id) AS unique_products,
    COUNT(DISTINCT seller_id) AS unique_sellers,
    count(distinct order_item_id) as order_iteams
FROM order_items;


SELECT
    SUM(order_id IS NULL) AS order_id_nulls,
    SUM(order_item_id IS NULL) AS order_item_id_nulls,
    SUM(product_id IS NULL) AS product_id_nulls,
    SUM(seller_id IS NULL) AS seller_id_nulls,
    SUM(price IS NULL) AS price_nulls,
    SUM(freight_value IS NULL) AS freight_nulls
FROM order_items;


-- ============================================================
-- 4. PAYMENTS - BASIC VALIDATION
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders
FROM payments;


SELECT
    SUM(order_id IS NULL) AS order_id_nulls,
    SUM(payment_type IS NULL) AS payment_type_nulls,
    SUM(payment_installments IS NULL) AS installments_nulls,
    SUM(payment_value IS NULL) AS payment_value_nulls
FROM payments;


-- ============================================================
-- 5. PRODUCTS - BASIC VALIDATION
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS unique_product_ids
FROM products;


SELECT
    SUM(product_id IS NULL) AS product_id_nulls,
    SUM(product_category_name IS NULL) AS category_nulls,
    SUM(product_weight_g IS NULL) AS weight_nulls,
    SUM(product_length_cm IS NULL) AS length_nulls,
    SUM(product_height_cm IS NULL) AS height_nulls,
    SUM(product_width_cm IS NULL) AS width_nulls
FROM products;


-- ============================================================
-- PART 2: RELATIONSHIP VALIDATION
-- ============================================================


-- Orders -> Customers

SELECT
    COUNT(*) AS orphan_orders
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- Order Items -> Orders

SELECT
    COUNT(*) AS orphan_order_items
FROM order_items oi
LEFT JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- Order Items -> Products

SELECT
    COUNT(*) AS orphan_products
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- Order Items -> Sellers

SELECT
    COUNT(*) AS orphan_sellers
FROM order_items oi
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;


-- Orders without payment

SELECT
    COUNT(*) AS orders_without_payment
FROM orders o
LEFT JOIN payments p
    ON o.order_id = p.order_id
WHERE p.order_id IS NULL;

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date
FROM orders o
LEFT JOIN payments p
    ON o.order_id = p.order_id
WHERE p.order_id IS NULL;
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.price,
    oi.freight_value
FROM order_items_clean oi
WHERE oi.order_id = 'bfbd0f9bdef84302105ad712db648a6c';


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


-- ------------------------------------------------------------
-- CLEANED CUSTOMERS
-- ------------------------------------------------------------

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


-- ------------------------------------------------------------
-- CLEANED ORDER ITEMS
-- ------------------------------------------------------------

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


-- ------------------------------------------------------------
-- CLEANED PAYMENTS
-- ------------------------------------------------------------
-- Invalid negative payment values are converted to NULL.
-- We do NOT delete the entire payment record.
-- ------------------------------------------------------------

DROP TABLE IF EXISTS payments_clean;

CREATE TABLE payments_clean AS
SELECT
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    CASE
        WHEN payment_value >= 0 THEN payment_value
        ELSE NULL
    END AS payment_value
FROM payments
WHERE order_id IS NOT NULL;


-- ------------------------------------------------------------
-- CLEANED PRODUCTS
-- ------------------------------------------------------------
-- Invalid/non-positive physical measurements are converted
-- to NULL rather than deleting the product.
-- ------------------------------------------------------------

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
-- PART 10: POST-CLEANING VALIDATION
-- ============================================================


-- Clean orders

SELECT
    COUNT(*) AS clean_orders,
    COUNT(DISTINCT order_id) AS unique_orders
FROM orders_clean;


-- Clean customers

SELECT
    COUNT(*) AS clean_customer_rows,
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers_clean;


-- Clean order items

SELECT
    COUNT(*) AS clean_order_items,
    SUM(price < 0) AS negative_prices,
    SUM(freight_value < 0) AS negative_freight
FROM order_items_clean;


-- Clean payments

SELECT
    COUNT(*) AS clean_payment_rows,
    SUM(payment_value < 0) AS negative_payments
FROM payments_clean;


-- Clean products

SELECT
    COUNT(*) AS clean_products,
    SUM(product_weight_g <= 0) AS invalid_weights,
    SUM(product_length_cm <= 0) AS invalid_lengths,
    SUM(product_height_cm <= 0) AS invalid_heights,
    SUM(product_width_cm <= 0) AS invalid_widths
FROM products_clean;


-- ============================================================
-- PART 11: CLEAN TABLE RELATIONSHIP VALIDATION
-- ============================================================


-- Orders -> Customers

SELECT
    COUNT(*) AS orphan_orders
FROM orders_clean o
LEFT JOIN customers_clean c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- Order Items -> Orders

SELECT
    COUNT(*) AS orphan_order_items
FROM order_items_clean oi
LEFT JOIN orders_clean o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- Order Items -> Products

SELECT
    COUNT(*) AS orphan_products
FROM order_items_clean oi
LEFT JOIN products_clean p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- ============================================================
-- PART 12: FINAL CLEAN DATASET SUMMARY
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


