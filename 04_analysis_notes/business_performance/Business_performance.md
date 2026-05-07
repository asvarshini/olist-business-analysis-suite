Business Performance Analysis Notes

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