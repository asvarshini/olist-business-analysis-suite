# 📊 Olist Business Analysis Suite

### End-to-End E-Commerce Business Intelligence | SQL • Python • Streamlit • Plotly

> Transforming **99K+ Brazilian e-commerce orders** into actionable business insights through data validation, SQL analytics, customer segmentation, revenue analysis, and an interactive Streamlit dashboard.

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-MySQL-orange?logo=mysql)](https://www.mysql.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly)](https://plotly.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?logo=github)](https://github.com/)

</p>

<p align="center">

### 🚀 <a href="https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/">View Live Dashboard</a>

</p>

---

## 🌟 Project Overview

The **Olist Business Analysis Suite** is an end-to-end business intelligence project built using the Brazilian Olist e-commerce dataset.

The project combines **SQL data analysis, data validation and cleaning, Python-based processing, customer analytics, and an interactive Streamlit dashboard** to answer practical business questions.

### 🎯 Business Questions

This project investigates:

* 💰 How much revenue is being generated?
* 📈 How does revenue change over time?
* 🛍️ Which product categories generate the most revenue?
* 🗺️ Which Brazilian states contribute the most revenue?
* 📦 What is the distribution of order statuses?
* 👥 How many unique customers are there?
* 🔁 What percentage of customers make repeat purchases?
* ⭐ Which customers generate the highest lifetime revenue?
* 🧩 How can customers be segmented by purchase frequency?
* 🤝 Which product categories are frequently purchased together?

---

# 📌 Key Business Metrics

| KPI                                  |               Result |
| ------------------------------------ | -------------------: |
| 📦 Total Orders                      |           **99,441** |
| 👥 Unique Customers                  |           **96,096** |
| 💰 Total Payment Revenue             | **R$ 16,008,872.12** |
| 📈 Average Order Payment             |        **R$ 160.99** |
| 🏷️ Product Categories               |               **71** |
| 🚚 Delivered Orders                  |  **96,478 (97.02%)** |
| 🔁 Repeat Customer Rate              |            **3.12%** |
| 🏆 Highest Customer Lifetime Revenue |     **R$ 13,664.08** |

> **Metric note:** `customer_id` identifies the customer record associated with an order, while `customer_unique_id` identifies the actual customer across multiple orders. Customer-level metrics therefore use `customer_unique_id`.

---

# 🧹 Data Validation & Cleaning

Data quality was treated as an important part of the analysis rather than simply loading the CSV files and creating charts.

### 🔍 Validation performed

* NULL-value checks
* Duplicate checks
* Primary-key validation
* Foreign-key relationship checks
* Orphan-record checks
* Date validation
* Negative payment validation
* Negative price validation
* Negative freight validation
* Product dimension validation
* Order-status validation
* Review-score validation

### 🧼 Cleaning approach

The original raw datasets are preserved.

Instead of modifying the raw data directly, separate cleaned analysis tables/files were created.

This keeps the project reproducible and makes it possible to compare the original data with the analysis-ready version.

### Important principle

> **Not every NULL is an error.**

For example, an order that has not been delivered may legitimately have a missing delivery date. Such values should not automatically be deleted simply because they are NULL.

---

# 🗂️ Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The analysis works with the following major datasets:

| Dataset       | Purpose                             |
| ------------- | ----------------------------------- |
| `orders`      | Order lifecycle and timestamps      |
| `customers`   | Customer and geographic information |
| `order_items` | Products purchased within orders    |
| `payments`    | Payment transactions and values     |
| `products`    | Product and category information    |

### Customer identifiers

A key analytical distinction is made between:

```text
customer_id
      ↓
Customer record associated with an order

customer_unique_id
      ↓
Actual customer across multiple orders
```

Therefore:

```text
99,441 Orders
        ↓
96,096 Unique Customers
```

This distinction is particularly important for repeat-purchase and customer-segmentation analysis.

---

# 📊 Revenue Analysis

## 💰 Total Payment Revenue

### **R$ 16,008,872.12**

Revenue is calculated from payment records:

```sql
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;
```

---

## 📈 Average Order Payment

### **R$ 160.99**

The dashboard calculates payment-based AOV by first aggregating payments at the order level.

```sql
SELECT
    ROUND(AVG(order_payment), 2) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment
    FROM payments
    GROUP BY order_id
) t;
```

> This is a **payment-based AOV**, which can differ from an AOV calculated using only product item prices.

---

# 🛍️ Top Product Categories

The top product categories by **product-item price revenue** are:

| Rank | Category                |             Revenue |
| ---: | ----------------------- | ------------------: |
| 🥇 1 | Beauty & Health         | **R$ 1,258,681.34** |
| 🥈 2 | Watches & Gifts         | **R$ 1,205,005.68** |
| 🥉 3 | Bed, Bath & Table       | **R$ 1,036,988.68** |
|    4 | Sports & Leisure        |   **R$ 988,048.97** |
|    5 | Computers & Accessories |   **R$ 911,954.32** |
|    6 | Furniture & Decoration  |   **R$ 729,762.49** |
|    7 | Cool Stuff              |   **R$ 635,290.85** |
|    8 | Housewares              |   **R$ 632,248.66** |
|    9 | Automotive              |   **R$ 592,720.11** |
|   10 | Garden Tools            |   **R$ 485,256.46** |

### 🏆 Top Category

**Beauty & Health**

Product-item revenue:

### **R$ 1,258,681.34**

> Category revenue is based on `order_items.price`, while total company revenue is based on `payments.payment_value`. These metrics measure different components of the business and should not be directly treated as identical.

---

# 🗺️ Geographic Revenue Analysis

### 🥇 São Paulo (SP)

São Paulo is the highest-revenue state in the analysis.

**State Revenue:**

### **R$ 5,998,226.96**

**Share of total payment revenue:**

### **37.47%**

This highlights São Paulo as a major geographic market for the business.

---

# 📦 Order Performance

## Total Orders

### **99,441**

Calculated using distinct order IDs:

```sql
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;
```

---

## 🚚 Order Status Distribution

| Status      |     Orders | Percentage |
| ----------- | ---------: | ---------: |
| Delivered   | **96,478** | **97.02%** |
| Shipped     |      1,107 |      1.11% |
| Canceled    |        625 |      0.63% |
| Unavailable |        609 |      0.61% |
| Invoiced    |        314 |      0.32% |
| Processing  |        301 |      0.30% |
| Created     |          5 |      0.01% |
| Approved    |          2 |      0.00% |

### Key takeaway

The dataset shows a very high proportion of orders reaching the **delivered** status.

---

# 📅 Order Trends

The dashboard provides monthly order-volume analysis using:

```sql
SELECT
    DATE_FORMAT(
        order_purchase_timestamp,
        '%Y-%m'
    ) AS monthly_purchase,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY monthly_purchase
ORDER BY monthly_purchase;
```

This allows the business to identify:

* Seasonal demand
* Monthly growth patterns
* High-volume periods
* Changes in purchasing activity

---

# 👥 Customer Analytics

## Unique Customers

### **96,096**

Customer-level analysis uses:

```text
customer_unique_id
```

rather than simply counting `customer_id`.

This prevents customers with multiple order records from being treated as completely separate customers.

---

# 🔁 Repeat Customer Analysis

### Repeat Customer Rate: **3.12%**

Customers were classified based on the number of distinct orders associated with their `customer_unique_id`.

```sql
SELECT
    COUNT(*) AS total_customers,
    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN purchase_count > 1
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
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
```

### Business implication

The relatively low repeat-purchase rate suggests a potential opportunity to improve:

* Customer retention
* Personalized marketing
* Re-engagement campaigns
* Loyalty programs
* Cross-selling
* Post-purchase communication

---

# 🎯 Customer Segmentation

Customers are segmented according to purchase frequency:

| Segment             | Definition |  Customers |      Share |
| ------------------- | ---------- | ---------: | ---------: |
| 🟢 Low Frequency    | 1 order    | **93,099** | **96.88%** |
| 🟡 Medium Frequency | 2–5 orders |  **2,986** |  **3.11%** |
| 🔵 High Frequency   | 6+ orders  |     **11** |  **0.01%** |

### Key insight

The overwhelming majority of customers belong to the **Low Frequency** segment.

This creates a clear business opportunity around converting one-time buyers into repeat customers.

---

# 🏆 Top Customer Lifetime Revenue

The highest customer lifetime revenue identified in the analysis is:

### **R$ 13,664.08**

Customer lifetime revenue is calculated by aggregating payment values using `customer_unique_id`.

```sql
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
```

This analysis helps identify high-value customers who may be suitable for targeted retention strategies.

---

# 🤖 Product Recommendation Analysis

The dashboard also includes a lightweight **co-purchase analysis**.

It identifies product categories that frequently appear together within the same order.

### Features

* 🔗 Frequently bought-together categories
* 🧩 Category combinations
* 📊 Items-per-order distribution
* 🛍️ Categories with highest order presence
* 💡 Interactive recommendation exploration

### Example workflow

```text
Customer purchases Category A
            ↓
Find categories purchased
in the same order
            ↓
Rank category combinations
            ↓
Generate recommendation candidates
```

> The recommendation section is an analytical co-purchase engine, not a machine-learning recommendation model.

---

# 🖥️ Interactive Dashboard

The Streamlit dashboard contains five major sections:

### 📈 1. Revenue

* Total revenue
* Monthly revenue trend
* Top product categories

### 📦 2. Orders

* Total orders
* Monthly order volume
* Order status distribution

### 👥 3. Customers

* Customer segmentation
* Customers by state
* Customer frequency analysis

### 🤖 4. Recommendations

* Frequently purchased categories
* Cross-category buying patterns
* Product recommendation exploration

### 📝 5. SQL Showcase

* Revenue SQL
* Order SQL
* Customer SQL
* Customer segmentation
* Lifetime revenue
* SQL skills demonstrated

---

# 🚀 Live Dashboard

## 👉 [Open the Olist Business Analysis Dashboard](https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/)

The dashboard is deployed using Streamlit and can be explored interactively.

---

# 🛠️ Technology Stack

| Technology      | Purpose                               |
| --------------- | ------------------------------------- |
| 🐍 Python       | Data processing and dashboard logic   |
| 🐼 Pandas       | Data manipulation                     |
| 🗄️ MySQL / SQL | Data validation and business analysis |
| 📊 Plotly       | Interactive visualizations            |
| 🎨 Streamlit    | Interactive dashboard                 |
| 🔧 Git          | Version control                       |
| 🐙 GitHub       | Project management and portfolio      |

---

# 🧠 SQL Skills Demonstrated

This project demonstrates practical SQL skills including:

### Data Quality

* NULL validation
* Duplicate detection
* Primary-key validation
* Foreign-key validation
* Orphan-record detection
* Range validation

### Data Analysis

* `SELECT`
* `WHERE`
* `GROUP BY`
* `ORDER BY`
* `HAVING`
* `COUNT()`
* `COUNT(DISTINCT ...)`
* `SUM()`
* `AVG()`
* `ROUND()`
* `CASE`
* Subqueries
* Multi-table joins
* Date functions

### Business Analytics

* Revenue analysis
* Customer segmentation
* Repeat customer analysis
* Customer lifetime value
* Geographic analysis
* Product category analysis
* Order-status analysis
* Time-series analysis

---

# 🐍 Python Skills Demonstrated

* Pandas data processing
* CSV ingestion
* Datetime transformation
* Filtering
* GroupBy analysis
* Data merging
* Unique-value analysis
* Streamlit application development
* Plotly visualization
* Interactive filtering
* Cached data loading

---

# 📁 Project Structure

```text
Olist-Business-Analysis-Suite/
│
├── 01_dataset/
│   └── 00_raw_data/
│       ├── olist_orders_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_customers_dataset.csv
│       ├── olist_products_dataset.csv
│       └── cleaned_files/
│
├── 02_schema_design/
│
├── 03_sql_queries/
│   ├── data_validation_cleaning.sql
│   ├── revenue_analysis.sql
│   ├── order_performance.sql
│   └── customer_performance.sql
│
├── 04_analysis_notes/
│
├── 05_dashboards/
│   └── customer_dashboard/
│
├── dashboard.py
├── requirements.txt
└── README.md
```

> File and folder names may vary slightly depending on the final repository structure.

---

# 🔄 End-to-End Workflow

```text
             RAW OLIST DATA
                    │
                    ▼
          ┌───────────────────┐
          │ Data Exploration  │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Data Validation   │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Data Cleaning     │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ SQL Analysis      │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Business Insights │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Python / Pandas   │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Streamlit + Plotly│
          └─────────┬─────────┘
                    │
                    ▼
             LIVE DASHBOARD
```

---

# 💡 Key Business Insights

### 1️⃣ Strong Delivery Performance

**97.02%** of orders reached the delivered status, indicating strong overall order fulfillment performance within the dataset.

### 2️⃣ Large One-Time Customer Segment

**96.88%** of customers are classified as low-frequency customers with only one order.

This creates a significant opportunity for customer retention initiatives.

### 3️⃣ São Paulo Is a Major Market

São Paulo contributes approximately **37.47%** of total payment revenue, making it the most significant state in the analysis.

### 4️⃣ Beauty & Health Leads Product Revenue

Beauty & Health generated approximately **R$ 1.26M** in product-item revenue, making it the top category in the analysis.

### 5️⃣ High-Value Customers Exist Despite Low Repeat Rate

The highest identified customer lifetime revenue is **R$ 13,664.08**, demonstrating that a small group of customers can contribute substantial value.

---

# 🎯 Business Recommendations

Based on the analysis, potential business actions include:

### 🔁 Improve Customer Retention

Develop targeted campaigns for one-time customers to encourage second purchases.

### 🎁 Loyalty Programs

Create incentives for customers moving from low-frequency to medium-frequency purchasing behavior.

### 🛍️ Cross-Selling

Use category co-purchase patterns to recommend complementary products.

### 🗺️ Geographic Marketing

Prioritize high-revenue states while investigating growth opportunities in lower-performing regions.

### ⭐ VIP Customer Strategy

Identify high-lifetime-value customers and develop personalized retention campaigns.

---

# 📌 Analytical Notes

### Orders vs Customers

These are intentionally different metrics:

```text
99,441
Total Orders
      │
      ▼
96,096
Unique Customers
```

A customer can place multiple orders, so the number of orders should not be interpreted as the number of customers.

### Revenue Definitions

This project uses different revenue concepts depending on the analysis:

```text
Payment Revenue
    ↓
payments.payment_value

Product Category Revenue
    ↓
order_items.price
```

These should not be treated as interchangeable metrics.

---

# 🧪 Reproducibility

To run the dashboard locally:

### 1. Clone the repository

```bash
git clone https://github.com/asvarshini/sql-data-portfolio.git
```

### 2. Navigate to the project

```bash
cd sql-data-portfolio
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit

```bash
streamlit run dashboard.py
```

Make sure the required Olist CSV files are available under:

```text
01_dataset/00_raw_data/
```

---

# 📚 Project Learning Outcomes

Through this project, I strengthened my ability to:

* Work with large relational datasets
* Validate real-world data quality
* Build analysis-ready datasets
* Write business-focused SQL queries
* Analyze customer behavior
* Calculate revenue KPIs
* Perform customer segmentation
* Translate SQL results into business insights
* Build interactive dashboards
* Deploy analytical applications
* Document an end-to-end analytics project

---

# 👩‍💻 Author

## Varshini A S

**Data Science & AI | Data Analytics | SQL | Python | Business Intelligence**

🎓 Data Science & AI Program — IIT Roorkee
💻 Computer Science Engineering
🌱 GSSoC 2026 Contributor

### Interested in:

* Data Analyst Internships
* Business Analyst Internships
* Data Science Internships
* Analytics Projects
* Startup Opportunities

---

## ⭐ If you found this project useful

Feel free to explore the repository, try the live dashboard, and connect with me.

**Built with SQL + Python + Streamlit + Plotly**

### 🚀 [View Live Dashboard](https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/)
