#Business Performance Analysis Notes

Revenue Performance Analysis

Objective

The goal of this analysis was to understand overall business revenue performance using transaction-level payment data.

---

KPIs Analyzed

1. Total Company Revenue

Calculated total revenue generated from all customer payments using the payments table.

2. Monthly Revenue Trend

Analyzed how company revenue changed over time using order purchase timestamps and payment values.

3. Product Category Revenue

Identified product categories generating the highest revenue using product and order item data.

4. State-wise Revenue Analysis

Analyzed which customer states contributed the highest revenue to the business.

5. Top Customer Revenue Analysis

Identified high-value customers based on total lifetime transaction revenue.

---

Business Understanding

- Revenue analysis requires combining transaction data with business dimensions such as time, geography, products, and customers.
- Different revenue perspectives require different tables and aggregation logic.
- payments table represents transaction-level business revenue.
- order_items table helps analyze product-level revenue contribution.
- customers table enables regional business analysis.

---

Key Learning

- Learned how to perform KPI-based business analysis using SQL.
- Improved understanding of joins, aggregation, grouping, and time-based analysis.
- Understood the importance of selecting the correct revenue source based on business context.

## Order Performance Analysis

KPIs Analyzed

1. Total Orders

Calculated the total number of unique orders placed across the platform.

2. Total Product Orders

Analyzed the total number of products purchased through order items.

3. Monthly Order Trend

Evaluated how customer order activity changed over time using purchase timestamps.

4. Average Orders Per Customer

Calculated the average number of orders placed by each customer using nested aggregation.

5. Order Status Distribution

Analyzed operational order statuses such as delivered, canceled, shipped, and unavailable orders.

6. Average Order Value (AOV)

Calculated the average revenue generated per order transaction.

---

Business Understanding

- Order analysis helps measure business activity and operational performance.
- Monthly order trends help identify platform growth and customer purchasing patterns.
- Order status distribution reflects fulfillment efficiency and operational health.
- Average Order Value (AOV) helps evaluate customer basket size and transaction quality.

---

Key Learning

- Learned order-level vs item-level analysis.
- Improved understanding of nested aggregation using subqueries.
- Practiced KPI-based operational analysis using SQL.