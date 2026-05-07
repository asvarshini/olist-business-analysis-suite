-- =====================================================
-- BUSINESS PERFORMANCE ANALYSIS
-- Revenue Analysis
-- =====================================================
-- TABLE EXPLORATION

SELECT *
FROM orders
LIMIT 10;

SELECT COUNT(*)
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

-- KPI 1 : TOTAL COMPANY REVENUE

SELECT
ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;

-- KPI 2 : MONTHLY REVENUE TREND

SELECT
DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS monthly_trend,
ROUND(SUM(p.payment_value), 2) AS monthly_revenue
FROM orders o
JOIN payments p
ON p.order_id = o.order_id
GROUP BY monthly_trend
ORDER BY monthly_trend;