-- ============================================================
-- OLIST BUSINESS ANALYSIS SUITE
-- BUSINESS INSIGHTS & DERIVED METRICS
-- ============================================================
--
-- Purpose:
-- This file contains the final business metrics that are derived
-- from the detailed SQL analysis.
--
-- Use this file as the source of truth for:
--   • Revenue contribution
--   • Product category contribution
--   • Monthly growth
--   • Order status percentages
--   • Customer retention
--   • Customer segmentation
--   • Top customers
--   • Product/category performance
--
-- Database: MySQL
-- Dataset: Brazilian Olist E-Commerce
-- ============================================================


-- ============================================================
-- 1. DATASET OVERVIEW
-- ============================================================

-- Total rows in orders table
SELECT
    COUNT(*) AS total_order_rows
FROM orders;


-- Total unique orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- Total unique customer records
SELECT
    COUNT(DISTINCT customer_id) AS unique_customer_records
FROM customers;


-- Total actual unique customers
SELECT
    COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;


-- Total unique products
SELECT
    COUNT(DISTINCT product_id) AS unique_products
FROM products;


-- Total product categories
SELECT
    COUNT(DISTINCT product_category_name) AS product_categories
FROM products
WHERE product_category_name IS NOT NULL;


-- ============================================================
-- 2. TOTAL PAYMENT REVENUE
-- ============================================================

SELECT
    ROUND(SUM(payment_value), 2) AS total_payment_revenue
FROM payments;


-- Expected verified result:
-- R$ 16,008,872.12


-- ============================================================
-- 3. AVERAGE PAYMENT VALUE PER ORDER
-- ============================================================
--
-- First aggregate all payments belonging to each order.
-- Then calculate the average order payment.
-- ============================================================

SELECT
    ROUND(AVG(order_payment), 2) AS average_order_payment
FROM (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment
    FROM payments
    GROUP BY order_id
) AS order_totals;


-- Expected verified result:
-- Approximately R$ 160.99


-- ============================================================
-- 4. REVENUE BY BRAZILIAN STATE
-- ============================================================

SELECT
    c.customer_state,
    ROUND(SUM(p.payment_value), 2) AS state_revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY state_revenue DESC;


-- ============================================================
-- 5. STATE REVENUE CONTRIBUTION %
-- ============================================================
--
-- This calculates what percentage of TOTAL PAYMENT REVENUE
-- each state contributes.
-- ============================================================

SELECT
    c.customer_state,
    ROUND(SUM(p.payment_value), 2) AS state_revenue,

    ROUND(
        100.0 * SUM(p.payment_value)
        / (SELECT SUM(payment_value) FROM payments),
        2
    ) AS revenue_contribution_pct

FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN payments p
    ON o.order_id = p.order_id

GROUP BY c.customer_state
ORDER BY state_revenue DESC;


-- For São Paulo:
-- State Revenue ≈ R$ 5,998,226.96
-- Contribution ≈ 37.47%


-- ============================================================
-- 6. TOP STATE BUSINESS INSIGHT
-- ============================================================
--
-- Returns the highest-revenue state together with its
-- percentage contribution.
-- ============================================================

SELECT
    customer_state,
    state_revenue,
    revenue_contribution_pct
FROM (
    SELECT
        c.customer_state,

        ROUND(SUM(p.payment_value), 2) AS state_revenue,

        ROUND(
            100.0 * SUM(p.payment_value)
            / (SELECT SUM(payment_value) FROM payments),
            2
        ) AS revenue_contribution_pct

    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN payments p
        ON o.order_id = p.order_id

    GROUP BY c.customer_state
) AS state_summary

ORDER BY state_revenue DESC
LIMIT 1;


-- ============================================================
-- 7. PRODUCT CATEGORY REVENUE
-- ============================================================
--
-- Product category revenue is based on product item price.
-- ============================================================

SELECT
    pr.product_category_name,

    ROUND(SUM(oi.price), 2) AS category_revenue

FROM products pr
JOIN order_items oi
    ON oi.product_id = pr.product_id

WHERE pr.product_category_name IS NOT NULL

GROUP BY pr.product_category_name
ORDER BY category_revenue DESC;


-- ============================================================
-- 8. PRODUCT CATEGORY REVENUE CONTRIBUTION %
-- ============================================================
--
-- IMPORTANT:
-- The denominator here is TOTAL PRODUCT-ITEM REVENUE,
-- not total payment revenue.
--
-- This is the mathematically consistent way to calculate
-- category contribution.
-- ============================================================

SELECT
    pr.product_category_name,

    ROUND(SUM(oi.price), 2) AS category_revenue,

    ROUND(
        100.0 * SUM(oi.price)
        /
        (
            SELECT SUM(oi2.price)
            FROM order_items oi2
        ),
        2
    ) AS category_revenue_pct

FROM products pr
JOIN order_items oi
    ON oi.product_id = pr.product_id

WHERE pr.product_category_name IS NOT NULL

GROUP BY pr.product_category_name
ORDER BY category_revenue DESC;


-- ============================================================
-- 9. TOP PRODUCT CATEGORY
-- ============================================================

SELECT
    product_category_name,
    category_revenue,
    category_revenue_pct
FROM (
    SELECT
        pr.product_category_name,

        ROUND(SUM(oi.price), 2) AS category_revenue,

        ROUND(
            100.0 * SUM(oi.price)
            /
            (
                SELECT SUM(oi2.price)
                FROM order_items oi2
            ),
            2
        ) AS category_revenue_pct

    FROM products pr
    JOIN order_items oi
        ON oi.product_id = pr.product_id

    WHERE pr.product_category_name IS NOT NULL

    GROUP BY pr.product_category_name
) AS category_summary

ORDER BY category_revenue DESC
LIMIT 1;


-- Expected top category:
-- beleza_saude / Beauty & Health
-- Revenue ≈ R$ 1,258,681.34


-- ============================================================
-- 10. MONTHLY ORDER VOLUME
-- ============================================================

SELECT
    DATE_FORMAT(
        order_purchase_timestamp,
        '%Y-%m'
    ) AS purchase_month,

    COUNT(DISTINCT order_id) AS total_orders

FROM orders

GROUP BY purchase_month
ORDER BY purchase_month;


-- ============================================================
-- 11. TOP ORDER MONTH
-- ============================================================

SELECT
    purchase_month,
    total_orders
FROM (
    SELECT
        DATE_FORMAT(
            order_purchase_timestamp,
            '%Y-%m'
        ) AS purchase_month,

        COUNT(DISTINCT order_id) AS total_orders

    FROM orders

    GROUP BY purchase_month
) AS monthly_orders

ORDER BY total_orders DESC
LIMIT 1;


-- Expected:
-- November 2017
-- 7,544 orders


-- ============================================================
-- 12. MONTH-OVER-MONTH ORDER GROWTH
-- ============================================================
--
-- This tells us exactly how much order volume increased or
-- decreased compared with the previous month.
-- ============================================================

WITH monthly_orders AS (

    SELECT
        DATE_FORMAT(
            order_purchase_timestamp,
            '%Y-%m'
        ) AS purchase_month,

        COUNT(DISTINCT order_id) AS total_orders

    FROM orders

    GROUP BY purchase_month
),

monthly_growth AS (

    SELECT
        purchase_month,
        total_orders,

        LAG(total_orders) OVER (
            ORDER BY purchase_month
        ) AS previous_month_orders

    FROM monthly_orders
)

SELECT
    purchase_month,
    total_orders,
    previous_month_orders,

    ROUND(
        100.0 *
        (total_orders - previous_month_orders)
        / NULLIF(previous_month_orders, 0),
        2
    ) AS month_over_month_growth_pct

FROM monthly_growth

ORDER BY purchase_month;


-- ============================================================
-- 13. NOVEMBER 2017 MONTH-OVER-MONTH GROWTH
-- ============================================================
--
-- Use this query if the business statement is:
--
-- "November 2017 increased by X% compared with October 2017."
-- ============================================================

WITH monthly_orders AS (

    SELECT
        DATE_FORMAT(
            order_purchase_timestamp,
            '%Y-%m'
        ) AS purchase_month,

        COUNT(DISTINCT order_id) AS total_orders

    FROM orders

    GROUP BY purchase_month
)

SELECT
    purchase_month,
    total_orders,
    previous_month_orders,

    ROUND(
        100.0 *
        (total_orders - previous_month_orders)
        / NULLIF(previous_month_orders, 0),
        2
    ) AS growth_pct

FROM (
    SELECT
        purchase_month,
        total_orders,

        LAG(total_orders) OVER (
            ORDER BY purchase_month
        ) AS previous_month_orders

    FROM monthly_orders
) AS growth

WHERE purchase_month = '2017-11';


-- IMPORTANT:
-- Do NOT write "November increased by 36.7%"
-- unless this query actually returns 36.70%.
--
-- This query tells us the exact verified percentage.


-- ============================================================
-- 14. NOVEMBER 2017 VS AVERAGE MONTHLY ORDERS
-- ============================================================
--
-- This answers a DIFFERENT question:
--
-- "How much higher was November 2017 compared with the
-- average monthly order volume?"
-- ============================================================

WITH monthly_orders AS (

    SELECT
        DATE_FORMAT(
            order_purchase_timestamp,
            '%Y-%m'
        ) AS purchase_month,

        COUNT(DISTINCT order_id) AS total_orders

    FROM orders

    GROUP BY purchase_month
),

monthly_average AS (

    SELECT
        AVG(total_orders) AS average_monthly_orders

    FROM monthly_orders
)

SELECT
    m.purchase_month,
    m.total_orders,

    ROUND(a.average_monthly_orders, 2)
        AS average_monthly_orders,

    ROUND(
        100.0 *
        (m.total_orders - a.average_monthly_orders)
        / a.average_monthly_orders,
        2
    ) AS above_average_pct

FROM monthly_orders m
CROSS JOIN monthly_average a

WHERE m.purchase_month = '2017-11';


-- ============================================================
-- 15. ORDER STATUS DISTRIBUTION
-- ============================================================

SELECT
    order_status,
    COUNT(*) AS total_orders,

    ROUND(
        100.0 * COUNT(*)
        / (SELECT COUNT(*) FROM orders),
        2
    ) AS order_status_pct

FROM orders

GROUP BY order_status
ORDER BY total_orders DESC;


-- Expected verified delivered result:
-- Delivered ≈ 96,478
-- Delivered percentage ≈ 97.02%


-- ============================================================
-- 16. DELIVERED ORDER RATE
-- ============================================================

SELECT

    SUM(
        CASE
            WHEN order_status = 'delivered'
            THEN 1
            ELSE 0
        END
    ) AS delivered_orders,

    COUNT(*) AS total_orders,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN order_status = 'delivered'
                THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS delivered_rate_pct

FROM orders;


-- ============================================================
-- 17. CUSTOMER PURCHASE FREQUENCY
-- ============================================================

SELECT
    c.customer_unique_id,

    COUNT(DISTINCT o.order_id) AS order_count

FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id

GROUP BY c.customer_unique_id
ORDER BY order_count DESC;


-- ============================================================
-- 18. CUSTOMER SEGMENTATION
-- ============================================================

SELECT

    CASE
        WHEN order_count = 1
            THEN 'Low Frequency'

        WHEN order_count BETWEEN 2 AND 5
            THEN 'Medium Frequency'

        ELSE 'High Frequency'

    END AS customer_segment,

    COUNT(*) AS total_customers

FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count

    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id

    GROUP BY c.customer_unique_id

) AS customer_orders

GROUP BY customer_segment

ORDER BY total_customers DESC;


-- ============================================================
-- 19. CUSTOMER SEGMENTATION WITH PERCENTAGES
-- ============================================================
--
-- This is the query to use for the README and dashboard
-- segmentation percentages.
-- ============================================================

SELECT

    customer_segment,

    total_customers,

    ROUND(
        100.0 * total_customers
        / SUM(total_customers) OVER (),
        2
    ) AS customer_percentage

FROM (

    SELECT

        CASE
            WHEN order_count = 1
                THEN 'Low Frequency'

            WHEN order_count BETWEEN 2 AND 5
                THEN 'Medium Frequency'

            ELSE 'High Frequency'

        END AS customer_segment,

        COUNT(*) AS total_customers

    FROM (

        SELECT
            c.customer_unique_id,
            COUNT(DISTINCT o.order_id) AS order_count

        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id

        GROUP BY c.customer_unique_id

    ) AS customer_orders

    GROUP BY customer_segment

) AS segments

ORDER BY total_customers DESC;


-- Expected verified results:
--
-- Low Frequency      93,099    96.88%
-- Medium Frequency    2,986     3.11%
-- High Frequency         11     0.01%
--
-- Total               96,096   100.00%


-- ============================================================
-- 20. REPEAT CUSTOMER RATE
-- ============================================================

SELECT

    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN order_count > 1
            THEN 1
            ELSE 0
        END
    ) AS repeat_customers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN order_count > 1
                THEN 1
                ELSE 0
            END
        )
        / COUNT(*),
        2
    ) AS repeat_customer_rate_pct

FROM (

    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count

    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id

    GROUP BY c.customer_unique_id

) AS customer_orders;


-- Expected verified result:
-- Total customers: 96,096
-- Repeat customers: 2,997
-- Repeat customer rate: 3.12%


-- ============================================================
-- 21. TOP CUSTOMERS BY LIFETIME REVENUE
-- ============================================================

SELECT

    c.customer_unique_id,

    ROUND(
        SUM(p.payment_value),
        2
    ) AS customer_lifetime_revenue

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN payments p
    ON p.order_id = o.order_id

GROUP BY c.customer_unique_id

ORDER BY customer_lifetime_revenue DESC

LIMIT 10;


-- Expected highest customer lifetime revenue:
-- Approximately R$ 13,664.08


-- ============================================================
-- 22. TOP CUSTOMER
-- ============================================================

SELECT

    customer_unique_id,
    customer_lifetime_revenue

FROM (

    SELECT

        c.customer_unique_id,

        ROUND(
            SUM(p.payment_value),
            2
        ) AS customer_lifetime_revenue

    FROM orders o

    JOIN customers c
        ON o.customer_id = c.customer_id

    JOIN payments p
        ON p.order_id = o.order_id

    GROUP BY c.customer_unique_id

) AS customer_revenue

ORDER BY customer_lifetime_revenue DESC

LIMIT 1;


-- ============================================================
-- 23. UNIQUE PRODUCTS VS PRODUCT CATEGORIES
-- ============================================================
--
-- IMPORTANT:
-- These are two different business metrics.
--
-- Unique Products  = distinct product_id
-- Product Categories = distinct product_category_name
-- ============================================================

SELECT
    COUNT(DISTINCT product_id) AS unique_products,

    COUNT(
        DISTINCT product_category_name
    ) AS product_categories

FROM products
WHERE product_category_name IS NOT NULL;


-- Expected:
-- Unique Products: 32,951
-- Product Categories: 71


-- ============================================================
-- 24. TOP 10 PRODUCT CATEGORIES BY ORDER PRESENCE
-- ============================================================

SELECT

    p.product_category_name,

    COUNT(DISTINCT oi.order_id) AS orders_containing_category

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

WHERE p.product_category_name IS NOT NULL

GROUP BY p.product_category_name

ORDER BY orders_containing_category DESC

LIMIT 10;


-- ============================================================
-- 25. TOP 10 PRODUCT CATEGORIES BY ITEM REVENUE
-- ============================================================

SELECT

    p.product_category_name,

    ROUND(
        SUM(oi.price),
        2
    ) AS category_revenue

FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

WHERE p.product_category_name IS NOT NULL

GROUP BY p.product_category_name

ORDER BY category_revenue DESC

LIMIT 10;


-- ============================================================
-- 26. PRODUCTS WITH HIGHEST REVENUE
-- ============================================================

SELECT

    oi.product_id,

    ROUND(
        SUM(oi.price),
        2
    ) AS product_revenue,

    COUNT(DISTINCT oi.order_id) AS order_count

FROM order_items oi

GROUP BY oi.product_id

ORDER BY product_revenue DESC

LIMIT 10;


-- ============================================================
-- 27. REVENUE BY YEAR
-- ============================================================

SELECT

    YEAR(o.order_purchase_timestamp) AS purchase_year,

    ROUND(
        SUM(p.payment_value),
        2
    ) AS total_revenue

FROM orders o

JOIN payments p
    ON o.order_id = p.order_id

GROUP BY purchase_year

ORDER BY purchase_year;


-- ============================================================
-- 28. REVENUE BY MONTH
-- ============================================================

SELECT

    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS revenue_month,

    ROUND(
        SUM(p.payment_value),
        2
    ) AS monthly_revenue

FROM orders o

JOIN payments p
    ON o.order_id = p.order_id

GROUP BY revenue_month

ORDER BY revenue_month;


-- ============================================================
-- 29. TOP REVENUE MONTH
-- ============================================================

SELECT

    revenue_month,
    monthly_revenue

FROM (

    SELECT

        DATE_FORMAT(
            o.order_purchase_timestamp,
            '%Y-%m'
        ) AS revenue_month,

        ROUND(
            SUM(p.payment_value),
            2
        ) AS monthly_revenue

    FROM orders o

    JOIN payments p
        ON o.order_id = p.order_id

    GROUP BY revenue_month

) AS monthly_revenue_summary

ORDER BY monthly_revenue DESC

LIMIT 1;


-- ============================================================
-- 30. FINAL VERIFIED KPI SUMMARY
-- ============================================================
--
-- This section provides a quick reference for the main
-- project metrics.
-- ============================================================

SELECT
    (SELECT COUNT(DISTINCT order_id)
     FROM orders) AS total_orders,

    (SELECT COUNT(DISTINCT customer_unique_id)
     FROM customers) AS unique_customers,

    (SELECT COUNT(DISTINCT product_id)
     FROM products) AS unique_products,

    (SELECT COUNT(DISTINCT product_category_name)
     FROM products
     WHERE product_category_name IS NOT NULL)
     AS product_categories,

    (SELECT ROUND(SUM(payment_value), 2)
     FROM payments) AS total_payment_revenue;


-- ============================================================
-- END OF BUSINESS INSIGHTS
-- ============================================================