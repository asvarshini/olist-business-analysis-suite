# 📊 Olist Business Analysis Suite

> **End-to-end e-commerce business intelligence project analyzing 99K+ orders using SQL, Python, Pandas, Streamlit, and Plotly.**

<p align="center">

<a href="https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/">
<img src="https://img.shields.io/badge/🚀%20Live%20Dashboard-Streamlit-red?style=for-the-badge" alt="Live Dashboard"/>
</a>

<img src="https://img.shields.io/badge/SQL-MySQL-blue?style=for-the-badge&logo=mysql&logoColor=white" alt="SQL"/>
<img src="https://img.shields.io/badge/Python-Pandas-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Visualization-Plotly-blue?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly"/>

</p>

---

## 📌 Overview

The **Olist Business Analysis Suite** transforms raw Brazilian e-commerce data into actionable business insights.

The project covers the complete analytics workflow:

**Raw Data → Validation & Cleaning → SQL Analysis → Python Analysis → Business Insights → Interactive Dashboard**

The analysis focuses on **revenue, orders, products, customers, geographic performance, and purchasing behavior**.

🚀 **[Explore the Live Dashboard](https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/)**

---

## 📊 Key Metrics

| Metric | Result |
|---|---:|
| 📦 Total Orders | **99,441** |
| 💰 Total Payment Revenue | **R$ 16,008,872.12** |
| 📈 Average Order Payment | **R$ 160.99** |
| 👥 Unique Customers | **96,096** |
| 🚚 Delivered Orders | **97.02%** |
| 🔁 Repeat Customer Rate | **3.12%** |
| 🛍️ Product Categories | **71** |
|  🛍️ Unique Products |	**32,951** |
| ⭐ Top Customer Lifetime Revenue | **R$ 13,664.08** |

> **Note:** `order_id` represents an order, while `customer_unique_id` represents the actual customer across multiple orders. Therefore, orders and unique customers are different metrics.

---

## 🎯 Business Questions

This project answers questions such as:

- 💰 How much revenue does the business generate?
- 📈 How does revenue and order volume change over time?
- 🛍️ Which product categories perform best?
- 🗺️ Which states generate the most revenue?
- 👥 How many unique and repeat customers are there?
- 🔁 What does customer purchase frequency look like?
- ⭐ Who are the highest-value customers?
- 🤖 Which product categories are frequently purchased together?

---

## 🧹 Data Validation & Cleaning

Before analysis, the datasets were checked for data-quality issues including:

- NULL values
- Duplicate records
- Primary-key uniqueness
- Foreign-key relationships
- Orphan records
- Invalid dates
- Negative prices and payments
- Invalid product dimensions
- Order-status consistency

Cleaned analysis files were created while keeping the original raw datasets unchanged.

> The cleaning process preserves meaningful NULL values where they represent legitimate business conditions.

---

## 💰 Key Business Insights

### 🏆 Product Performance

**Beauty & Health** is the highest-performing product category by product-item revenue:

**R$ 1,258,681.34**

Other strong categories include:

- Watches & Gifts — R$ 1,205,005.68
- Bed, Bath & Table — R$ 1,036,988.68
- Sports & Leisure — R$ 988,048.97
- Computers & Accessories — R$ 911,954.32

### 🗺️ Geographic Performance

**São Paulo (SP)** is the largest revenue-generating state:

**R$ 5,998,226.96**

This represents approximately **37.47%** of total payment revenue.

### 📦 Order Performance

**97.02% of orders were delivered**, indicating strong overall fulfillment performance.

The highest monthly order volume occurred in:

**November 2017 — 7,544 orders**

### 👥 Customer Behavior

The analysis identified:

- **96,096 unique customers**
- **2,997 repeat customers**
- **3.12% repeat customer rate**

Customer frequency segmentation:

| Segment | Definition | Customers | Share |
|---|---|---:|---:|
| 🟢 Low Frequency | 1 order | 93,099 | 96.88% |
| 🟡 Medium Frequency | 2–5 orders | 2,986 | 3.11% |
| 🔵 High Frequency | 6+ orders | 11 | 0.01% |

### 💡 Business Opportunity

The large Low Frequency customer segment highlights an opportunity to improve retention through:

**Personalized offers • Loyalty programs • Product recommendations • Follow-up campaigns • Cross-selling**

---

## 🤖 Recommendation Analysis

The dashboard also includes co-purchase analysis to identify categories frequently purchased together.

This can support:

- 🛒 Cross-selling
- 📦 Product bundling
- 📧 Targeted marketing
- 🏷️ Promotional campaigns
- 🎯 Personalized recommendations

---

## 🚀 Interactive Dashboard

The Streamlit dashboard provides an interactive view of the analysis.

### Dashboard Features

| Section | Features |
|---|---|
| 🔍 Filters | Date range and state |
| 💰 Revenue | Revenue trends and top categories |
| 📦 Orders | Monthly volume and order status |
| 👥 Customers | Segmentation and state distribution |
| 🤖 Recommendations | Co-purchase and category analysis |
| 📝 SQL Showcase | SQL queries behind the analysis |

### 📊 KPI Cards

The dashboard displays:

**Revenue • Orders • AOV • Customers • Products**

🚀 **[Open the Live Dashboard](https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/)**

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐬 **MySQL / SQL** | Data validation, cleaning and business analysis |
| 🐍 **Python** | Data processing and analysis |
| 🐼 **Pandas** | Data manipulation |
| 📊 **Plotly** | Interactive visualizations |
| 🎈 **Streamlit** | Dashboard development |
| 🔧 **Git & GitHub** | Version control and project management |

---

## 🧠 SQL Skills Demonstrated

- Complex joins
- Aggregations with `SUM()`, `COUNT()`, `AVG()`
- `GROUP BY` and `HAVING`
- `DISTINCT` analysis
- Subqueries
- `CASE` statements
- Date functions
- Customer segmentation
- Ranking and analytical queries
- Data-quality validation
- Foreign-key and relationship checks

---

## 📂 Project Structure

```text
Olist-Business-Analysis-Suite/
│
├── 01_dataset/
│   └── 00_raw_data/
│            ├── Raw Olist CSV files
│    |___01_Cleaned_data/
│      └── Cleaned analysis files
│             ├── data_validation_cleaning.sql
│
├── 02_schema_design/
│
├── 03_sql_queries/
│   ├── revenue_analysis.sql
│   ├── order_performance.sql
│   └── customer_performance.sql
│
├── 04_analysis_notes/
│
├── 05_dashboards/
│   └── customer_dashboard/
│
└── README.md
