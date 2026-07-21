# 📊 Olist Business Analysis Suite

End-to-end SQL-based business intelligence project analyzing **100,000+ orders** from Brazilian e-commerce platform Olist.

**[🚀 Live Dashboard](https://olist-business-analysis-suite-bzbtyhtszhgf2gjsdcbdwq.streamlit.app/)**

---

## 📌 Project Overview

| Metric | Value |
|--------|-------|
| Total Orders Analyzed | 99,440 |
| Total Revenue | R$ 16,008,782 |
| Average Order Value | R$ 161 |
| Unique Customers | 99,440 |
| Product Categories | 71 |

---

## ⚙️ Tech Stack

- **SQL** (MySQL) — Complex queries, joins, CTEs, window functions
- **Python** — Pandas, data processing
- **Streamlit** — Interactive web dashboard
- **Plotly** — Data visualization


olist-business-analysis-suite/
├── 01_dataset/
│   └── 00_raw_data/              # Raw CSV files (9 datasets)
├── 02_schema_design/             # Database schema documentation
│   └── schema_notes.md
├── 03_sql_queries/               # Business analysis queries
│   ├── business_performance/
│   │   ├── 01_revenue_analysis.sql
│   │   ├── 02_order_performance.sql
│   │   └── 03_customer_performance.sql
│   ├── sales_dashboard/
│   ├── delivery_logistics/
│   ├── customer_segmentation/
│   └── customer_satisfaction/
├── 04_analysis_notes/            # Business insights
│   └── business_performance.md
├── 05_dashboards/
│   └── customer_dashboard/
│       └── dashboard.py           # Streamlit app (LIVE)
├── requirements.txt              # Python dependencies


---

## 📊 Key Business Insights

### 💰 Revenue Analysis
- **Top revenue month:** November 2017 (Black Friday effect)
- **Top product category:** Beauty & Health (18.2% of revenue)
- **Top state by revenue:** São Paulo (SP) — 42% of total revenue

### 📦 Order Performance
- **Order completion rate:** 97.2% delivered successfully
- **Average delivery time:** 12 days
- **Peak order month:** November 2017 (+34% vs average)

### 👥 Customer Insights
- **Repeat customer rate:** 6.5%
- **Customer segmentation:**
  - Low Frequency (1 order): 93.5%
  - Medium Frequency (2-5 orders): 6.0%
  - High Frequency (6+ orders): 0.5%
- **Top customer lifetime value:** R$ 13,664

---

## 🚀 Live Dashboard Features

| Feature | Description |
|---------|-------------|
| **Interactive Filters** | Date range picker, state dropdown |
| **KPI Cards** | Revenue, Orders, AOV, Customers, Products |
| **Revenue Tab** | Monthly trends, top categories, state-wise revenue |
| **Orders Tab** | Monthly volume, status distribution pie chart, AOV trend |
| **Customers Tab** | Segmentation pie chart, state-wise customer distribution |

---

## 🛠️ SQL Skills Demonstrated

| Skill | Example Query |
|-------|--------------|
| Complex Joins | 4-table joins (orders, customers, payments, items) |
| Aggregation | `SUM()`, `COUNT()`, `AVG()` with `GROUP BY` |
| Subqueries | Customer lifetime revenue calculation |
| Date Functions | `DATE_FORMAT()` for time-series analysis |
| Case Statements | Customer segmentation logic |
| Window Functions | Ranking and row numbering |


└── README.md                     # This file
## 📂 Project Structure
