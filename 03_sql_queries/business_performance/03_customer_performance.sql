-- =====================================================
-- BUSINESS PERFORMANCE ANALYSIS
-- Customer Performance Analysis
-- =====================================================

-- =====================================================
-- KPI 1 : REPEAT CUSTOMER RATE
-- =====================================================

SELECT
COUNT(*) AS total_customers,

ROUND(
    100.0 *
    SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)
    / COUNT(*),
    2
) AS repeat_customer_rate_pct

FROM (
SELECT
c.customer_unique_id,
COUNT(DISTINCT o.order_id) AS purchase_count
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.customer_unique_id
) t;

-- =====================================================
-- KPI 2 : HIGH-VALUE CUSTOMERS
-- =====================================================

SELECT
c.customer_unique_id,
ROUND(SUM(p.payment_value), 2) AS customer_lifetime_revenue

FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN payments p
ON p.order_id = o.order_id

GROUP BY c.customer_unique_id
ORDER BY customer_lifetime_revenue DESC
LIMIT 10;

-- =====================================================
-- KPI 3 : MOST ACTIVE CUSTOMERS
-- =====================================================

SELECT
c.customer_unique_id,
COUNT(DISTINCT o.order_id) AS total_orders_placed

FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id

GROUP BY c.customer_unique_id
ORDER BY total_orders_placed DESC
LIMIT 10;

-- =====================================================
-- KPI 4 : MONTHLY NEW CUSTOMER ACQUISITION
-- =====================================================

SELECT
DATE_FORMAT(first_order_date, '%Y-%m') AS acquisition_month,
COUNT(*) AS new_customers

FROM (
SELECT
c.customer_unique_id,
MIN(o.order_purchase_timestamp) AS first_order_date

FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id

GROUP BY c.customer_unique_id

) t

GROUP BY acquisition_month
ORDER BY acquisition_month;

-- =====================================================
-- KPI 5 : CUSTOMER AVERAGE ORDER VALUE (AOV)
-- =====================================================

SELECT
t.customer_unique_id,
ROUND(AVG(t.order_total), 2) AS avg_order_value

FROM (
SELECT
c.customer_unique_id,
o.order_id,
SUM(p.payment_value) AS order_total

FROM payments p
JOIN orders o
    ON p.order_id = o.order_id
JOIN customers c
    ON c.customer_id = o.customer_id

GROUP BY c.customer_unique_id, o.order_id

) t

GROUP BY t.customer_unique_id
ORDER BY avg_order_value DESC
LIMIT 10;

-- =====================================================
-- KPI 6 : STATE-WISE CUSTOMER DISTRIBUTION
-- =====================================================

SELECT
customer_state,
COUNT(DISTINCT customer_unique_id) AS total_customers

FROM customers

GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;

-- =====================================================
-- KPI 7 : LOW-ENGAGEMENT CUSTOMERS
-- =====================================================

SELECT
COUNT(*) AS low_engagement_customers

FROM (
SELECT
c.customer_unique_id,
COUNT(DISTINCT o.order_id) AS total_orders

FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id

GROUP BY c.customer_unique_id

) t

WHERE total_orders = 1;

-- =====================================================
-- KPI 8 : TOP CUSTOMER REVENUE CONTRIBUTION
-- =====================================================

SELECT
ROUND(
(
SELECT SUM(customer_revenue)
FROM (
SELECT
c.customer_unique_id,
SUM(p.payment_value) AS customer_revenue

            FROM payments p
            JOIN orders o
                ON p.order_id = o.order_id
            JOIN customers c
                ON c.customer_id = o.customer_id

            GROUP BY c.customer_unique_id
            ORDER BY customer_revenue DESC
            LIMIT 10
        ) top_customers
    )

    /

    (
        SELECT SUM(payment_value)
        FROM payments
    ) * 100,

2) AS top_customer_revenue_contribution_pct;

-- =====================================================
-- KPI 9 : CUSTOMER SEGMENTATION
-- =====================================================

SELECT
CASE
WHEN total_orders = 1 THEN 'Low Frequency'
WHEN total_orders BETWEEN 2 AND 5 THEN 'Medium Frequency'
ELSE 'High Frequency'
END AS customer_segment,

COUNT(*) AS total_customers

FROM (
SELECT
c.customer_unique_id,
COUNT(DISTINCT o.order_id) AS total_orders

FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id

GROUP BY c.customer_unique_id

) t

GROUP BY customer_segment
ORDER BY total_customers DESC;