-- =====================================================
-- BUSINESS PERFORMANCE ANALYSIS
-- Revenue Performance Analysis
-- =====================================================

-- =====================================================
-- TABLE EXPLORATION
-- =====================================================

SELECT *
FROM orders
LIMIT 10;

SELECT COUNT(*) AS total_orders
FROM orders;

SELECT *
FROM payments
LIMIT 10;

SELECT *
FROM customers
LIMIT 10;

SELECT *
FROM order_items
LIMIT 10;

-- =====================================================
-- KPI 1 : TOTAL COMPANY REVENUE
-- =====================================================

SELECT
ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;

-- =====================================================
-- KPI 2 : MONTHLY REVENUE TREND
-- =====================================================

SELECT
DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS revenue_month,
ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p
ON p.order_id = o.order_id
GROUP BY revenue_month
ORDER BY revenue_month;

-- =====================================================
-- KPI 3 : PRODUCT CATEGORY REVENUE
-- =====================================================

SELECT
pr.product_category_name,
ROUND(SUM(oi.price), 2) AS product_category_revenue
FROM products pr
JOIN order_items oi
ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name
ORDER BY product_category_revenue DESC
LIMIT 10;

-- =====================================================
-- KPI 4 : STATE-WISE REVENUE
-- =====================================================

SELECT
c.customer_state,
ROUND(SUM(p.payment_value), 2) AS state_revenue
FROM orders o
JOIN customers c
ON c.customer_id = o.customer_id
JOIN payments p
ON p.order_id = o.order_id
GROUP BY c.customer_state
ORDER BY state_revenue DESC
LIMIT 10;

-- =====================================================
-- KPI 5 : TOP CUSTOMER REVENUE
-- =====================================================

SELECT
c.customer_unique_id,
ROUND(SUM(p.payment_value), 2) AS customer_lifetime_revenue
FROM orders o
JOIN customers c
ON c.customer_id = o.customer_id
JOIN payments p
ON p.order_id = o.order_id
GROUP BY c.customer_unique_id
ORDER BY customer_lifetime_revenue DESC
LIMIT 10;