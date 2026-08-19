-- =====================================================
-- BUSINESS PERFORMANCE ANALYSIS
-- Order Performance Analysis
-- =====================================================

-- =====================================================
-- KPI 1 : TOTAL ORDERS
-- =====================================================

SELECT
COUNT(DISTINCT order_id) AS total_orders
FROM orders;

-- =====================================================
-- KPI 2 : TOTAL PRODUCT ORDERS
-- =====================================================

SELECT
COUNT(order_item_id) AS total_product_orders
FROM order_items;

-- =====================================================
-- KPI 3 : MONTHLY ORDER TREND
-- =====================================================

SELECT
DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS monthly_purchase,
COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY monthly_purchase
ORDER BY monthly_purchase;

-- =====================================================
-- KPI 4 : AVERAGE ORDER VALUE (AOV)
-- =====================================================

SELECT
    ROUND(AVG(order_payment), 2) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment
    FROM payments
    GROUP BY order_id
) t;

-- =====================================================
-- KPI 5 : ORDER STATUS DISTRIBUTION
-- =====================================================

SELECT
order_status,
COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- =====================================================
-- KPI 6 : AVERAGE ORDER VALUE (AOV)
-- =====================================================

SELECT
AVG(t.order_total) AS average_order_value
FROM (
SELECT
order_id,
SUM(price) AS order_total
FROM order_items
GROUP BY order_id
) t;
