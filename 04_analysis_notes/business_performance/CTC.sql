use olist_analysis;

-- which month having highest revenue how much it is contributing to taotal revenue
WITH monthly_revenue AS (
    SELECT 
        DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
        SUM(p.payment_value) AS monthly_amount
    FROM orders o
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
),
total_revenue AS (
    SELECT SUM(monthly_amount) AS total_amount 
    FROM monthly_revenue
)
SELECT 
    m.month AS Top_Month,
    ROUND(m.monthly_amount, 2) AS Total_Amount,
    ROUND((m.monthly_amount / t.total_amount) * 100, 2) AS Contribution_Percentage
FROM monthly_revenue m
CROSS JOIN total_revenue t
ORDER BY m.monthly_amount DESC
LIMIT 1;

-- which product_category having highest revenue via payment_value how much it is contributing to total revenue

WITH category_revenue AS (
    SELECT 
        p.product_category_name,
        SUM(m.payment_value) AS total_amounts
    FROM products p
    JOIN order_items o ON o.product_id = p.product_id
    JOIN payments m ON m.order_id = o.order_id
    GROUP BY p.product_category_name
),
grand_total AS (
    SELECT SUM(total_amounts) AS total_revenue 
    FROM category_revenue
)
SELECT 
    cr.product_category_name,
    ROUND(cr.total_amounts, 2) AS total_amounts,
    ROUND((cr.total_amounts / gt.total_revenue) * 100, 2) AS contribution_percentage
FROM category_revenue cr
CROSS JOIN grand_total gt
ORDER BY cr.total_amounts DESC;

-- -- which product_category having highest revenue via price how much it is contributing to total revenue

with cat_rev as
(
select 
p.product_category_name,round(sum(o.price),2) as rev_single_prod
from orders as a
join order_items o on o.order_id =a.order_id
join products p on o.product_id =p.product_id
group by p.product_category_name
order by rev_single_prod DESC
),
grand_rev as
(
select 
round(sum(rev_single_prod),2) as rev_total_prod
from cat_rev)
select
c.product_category_name,
round((c.rev_single_prod /g. rev_total_prod)*100,2) as total_per_contribution
from cat_rev c,grand_rev g
limit 1;

-- which month having highest order and how much it is contribu=uting to total_orders
with saparate_month_order as
(

select date_format(order_purchase_timestamp,"%Y-%m") as Date_of_order,
count(order_id) as total_orders
from orders
group by Date_of_order
order by total_orders DESC),
total_order as
(select sum(total_orders) as total
from saparate_month_order)
select
Date_of_order ,round((total_orders /total)*100,2)as per_contri_to_total_order
from saparate_month_order,total_order
limit 1;

--  repated customer purcase rate
with count_order as
(select customer_unique_id,count(customer_id) as times_purchased
from customers
group by customer_unique_id
order by times_purchased DESC
)
select
round(
(sum(case when times_purchased >1 then 1 else 0 end )/count(*) )*100,2) as repated_customer
from count_order;
 