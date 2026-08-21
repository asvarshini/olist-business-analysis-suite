import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Olist Business Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — FIXED GAPS & CLEAN LAYOUT
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }

    /* FIXED: Reduced top gap */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 1400px;
    }
    /* Tighten main content against sidebar */
    [data-testid="stAppViewContainer"] .st-emotion-cache-1jicfl2 {
        padding-left: 0.2rem !important;
    }

    /* Remove default streamlit padding */
    .st-emotion-cache-1jicfl2 {
        padding-top: 0rem;
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* ---------- HERO SECTION ---------- */
    .hero-container {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.12) 0%, rgba(99, 102, 241, 0.12) 100%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.4rem;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 1.2rem;
        position: relative;
        z-index: 1;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 0.9rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 100px;
        color: #e2e8f0;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }

    /* ---------- KPI CARDS ---------- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 0.8rem;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 1.2rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s;
        text-align: center;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(148, 163, 184, 0.25);
    }
    .kpi-icon {
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }
    .kpi-label {
        font-size: 0.7rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.1;
    }
    .kpi-desc {
        font-size: 0.7rem;
        color: #64748b;
        margin-top: 0.4rem;
    }
    .kpi-accent-1 { border-top: 3px solid #10b981; }
    .kpi-accent-2 { border-top: 3px solid #3b82f6; }
    .kpi-accent-3 { border-top: 3px solid #f59e0b; }
    .kpi-accent-4 { border-top: 3px solid #8b5cf6; }
    .kpi-accent-5 { border-top: 3px solid #ec4899; }
    .kpi-accent-6 { border-top: 3px solid #06b6d4; }

    /* ---------- SECTION HEADERS ---------- */
    .section-header {
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
    }
    .section-header-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-header-sub {
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* ---------- TABS ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15, 23, 42, 0.6);
        padding: 0.4rem;
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px !important;
        padding: 0 1.2rem;
        font-weight: 600;
        font-size: 0.85rem;
        color: #94a3b8;
        border: none !important;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(56,189,248,0.15)) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(129,140,248,0.25) !important;
    }

    /* ---------- CONTENT CARDS ---------- */
    .content-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }

    /* ---------- INSIGHT BOXES ---------- */
    .insight-box {
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        position: relative;
        overflow: hidden;
    }
    .insight-box::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
    }
    .insight-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
        color: #f8fafc;
    }
    .insight-text {
        color: #cbd5e1;
        font-size: 0.85rem;
        line-height: 1.6;
    }
    .theme-revenue { background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(5, 150, 105, 0.03)); border: 1px solid rgba(16, 185, 129, 0.15); }
    .theme-revenue::before { background: #10b981; }
    .theme-orders { background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(37, 99, 235, 0.03)); border: 1px solid rgba(59, 130, 246, 0.15); }
    .theme-orders::before { background: #3b82f6; }
    .theme-customers { background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(124, 58, 237, 0.03)); border: 1px solid rgba(139, 92, 246, 0.15); }
    .theme-customers::before { background: #8b5cf6; }
    .theme-recs { background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(217, 119, 6, 0.03)); border: 1px solid rgba(245, 158, 11, 0.15); }
    .theme-recs::before { background: #f59e0b; }
    .theme-sql { background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(79, 70, 229, 0.03)); border: 1px solid rgba(99, 102, 241, 0.15); }
    .theme-sql::before { background: #6366f1; }

    /* ---------- STAT CARDS ---------- */
    .stat-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin: 1rem 0;
    }
    .stat-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    .stat-number {
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ---------- SQL CARDS ---------- */
    .query-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .query-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.8rem;
        color: #818cf8;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .query-sql {
        color: #e2e8f0;
        font-size: 0.8rem;
        line-height: 1.7;
        white-space: pre-wrap;
        font-family: 'SF Mono', 'Fira Code', monospace;
    }

    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }
    .sidebar-header {
        padding: 0.8rem 0;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
    }

    /* ---------- FOOTER ---------- */
    .dashboard-footer {
        margin-top: 3rem;
        padding: 2rem;
        text-align: center;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        color: #64748b;
        font-size: 0.85rem;
    }
    .dashboard-footer .author {
        color: #94a3b8;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    .dashboard-footer .tagline {
        color: #818cf8;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* ---------- SCROLLBAR ---------- */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

    /* ---------- SIDEBAR COMPACT FIXES ---------- */
    [data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }
    [data-testid="stSidebar"] .stDateInput,
    [data-testid="stSidebar"] .stSelectbox {
        margin-bottom: -0.5rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        margin-bottom: 0.2rem !important;
    }

    /* Responsive */
    @media (max-width: 1200px) {
        .kpi-grid { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
        .stat-row { grid-template-columns: 1fr; }
        .hero-title { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    def get_data_path(filename):
        local_path = f"../../01_dataset/00_raw_data/{filename}"
        cloud_path = f"01_dataset/00_raw_data/{filename}"
        return local_path if os.path.exists(local_path) else cloud_path

    orders = pd.read_csv(get_data_path("olist_orders_dataset.csv"))
    order_items = pd.read_csv(get_data_path("olist_order_items_dataset.csv"))
    payments = pd.read_csv(get_data_path("olist_order_payments_dataset.csv"))
    customers = pd.read_csv(get_data_path("olist_customers_dataset.csv"))
    products = pd.read_csv(get_data_path("olist_products_dataset.csv"))

    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"], errors="coerce")
    orders["order_month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    
    return orders, order_items, payments, customers, products

# ============================================================
# LOAD DATA
# ============================================================

try:
    orders, order_items, payments, customers, products = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Ensure Olist CSV files are in `01_dataset/00_raw_data/`")
    data_loaded = False

# ============================================================
# MAIN APPLICATION
# ============================================================

if data_loaded:

    # ========================================================
    # HERO SECTION
    # ========================================================

    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">📊 Olist Business Analytics</div>
        <div class="hero-subtitle">End-to-end business intelligence analysis of Brazilian e-commerce performance</div>
        <div>
            <span class="hero-badge">📦 100K+ Orders</span>
            <span class="hero-badge">💰 Revenue Analytics</span>
            <span class="hero-badge">👥 Customer Intelligence</span>
            <span class="hero-badge">🤖 Recommendations</span>
            <span class="hero-badge">🧠 SQL Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================
    # SIDEBAR FILTERS
    # ========================================================

    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h3 style="color:#f8fafc; margin:0; font-size:1.1rem;">🔍 Filters</h3><p style="color:#94a3b8; font-size:0.75rem; margin:0;">Refine your analysis</p></div>', unsafe_allow_html=True)
        
        min_date = orders["order_purchase_timestamp"].min().date()
        max_date = orders["order_purchase_timestamp"].max().date()
        
        date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        
        states = ["All"] + sorted(customers["customer_state"].dropna().unique().tolist())
        selected_state = st.selectbox("Customer State", states)
        
        st.markdown("""
        <div style="margin-top: 1.5rem; padding: 0.8rem; background: rgba(99,102,241,0.08); border-radius: 10px; border: 1px solid rgba(99,102,241,0.15);">
            <div style="color: #c7d2fe; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.3rem;">💡 Tip</div>
            <div style="color: #94a3b8; font-size: 0.7rem;">Use filters to explore regional and temporal patterns.</div>
        </div>
        """, unsafe_allow_html=True)

    # Handle dates
    if len(date_range) == 2:
        start_date = pd.Timestamp(date_range[0])
        end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
    else:
        start_date = pd.Timestamp(min_date)
        end_date = pd.Timestamp(max_date) + pd.Timedelta(days=1)

    # ========================================================
    # FILTER LOGIC
    # ========================================================

    mask = (orders["order_purchase_timestamp"] >= start_date) & (orders["order_purchase_timestamp"] < end_date)
    filtered_orders = orders.loc[mask].copy()

    if selected_state != "All":
        state_customer_ids = customers.loc[customers["customer_state"] == selected_state, "customer_id"]
        filtered_orders = filtered_orders[filtered_orders["customer_id"].isin(state_customer_ids)]

    # Merges
    orders_with_payments = filtered_orders.merge(payments, on="order_id", how="left")
    orders_with_items = filtered_orders.merge(order_items, on="order_id", how="left")
    orders_full = filtered_orders.merge(customers, on="customer_id", how="left")

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_revenue = orders_with_payments["payment_value"].sum()
    total_orders = filtered_orders["order_id"].nunique()
    order_payment_totals = orders_with_payments.groupby("order_id")["payment_value"].sum()
    aov = order_payment_totals.mean()
    
    filtered_customer_ids = filtered_orders["customer_id"].dropna().unique()
    total_customers = customers[customers["customer_id"].isin(filtered_customer_ids)]["customer_unique_id"].nunique()
    total_products = orders_with_items["product_id"].nunique()
    total_categories = products["product_category_name"].nunique()

    # ========================================================
    # KPI CARDS — 6 CARDS WITH PRODUCT CATEGORY PROMINENT
    # ========================================================

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-accent-1">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">R$ {total_revenue:,.0f}</div>
            <div class="kpi-desc">Payment value</div>
        </div>
        <div class="kpi-card kpi-accent-2">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-desc">Unique order IDs</div>
        </div>
        <div class="kpi-card kpi-accent-3">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">R$ {aov:,.2f}</div>
            <div class="kpi-desc">Mean payment</div>
        </div>
        <div class="kpi-card kpi-accent-4">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Unique Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-desc">customer_unique_id</div>
        </div>
        <div class="kpi-card kpi-accent-5">
            <div class="kpi-icon">🛍️</div>
            <div class="kpi-label">Unique Products</div>
            <div class="kpi-value">{total_products:,}</div>
            <div class="kpi-desc">Distinct items sold</div>
        </div>
        <div class="kpi-card kpi-accent-6">
            <div class="kpi-icon">🏷️</div>
            <div class="kpi-label">Product Categories</div>
            <div class="kpi-value">{total_categories}</div>
            <div class="kpi-desc">Total categories</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Revenue", "📦 Orders", "👥 Customers", "🤖 Recommendations", "🧠 SQL Showcase"
    ])

    # ========================================================
    # TAB 1 — REVENUE (Emerald Theme)
    # ========================================================

    with tab1:
        st.markdown("""
        <div class="section-header">
            <div class="section-header-title"><span style="color:#10b981;">💰</span> Revenue Performance</div>
            <div class="section-header-sub">Track revenue trends and category contributions</div>
        </div>
        """, unsafe_allow_html=True)

        monthly_rev = orders_with_payments.groupby("order_month")["payment_value"].sum().reset_index()
        
        fig = px.area(
            monthly_rev, x="order_month", y="payment_value",
            markers=True, title=None, color_discrete_sequence=["#10b981"]
        )
        fig.update_layout(
            template="plotly_dark", height=380,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="Month", yaxis_title="Revenue (R$)",
            font=dict(family="Inter, sans-serif", size=12),
            title=dict(font=dict(size=14, color="#f8fafc"))
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=5))
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="section-header" style="margin-top:1rem;">
            <div class="section-header-title"><span style="color:#10b981;">🏷️</span> Top Product Categories</div>
            <div class="section-header-sub">Highest revenue-generating product segments</div>
        </div>
        """, unsafe_allow_html=True)

        items_prod = orders_with_items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        cat_rev = items_prod.groupby("product_category_name")["price"].sum().reset_index().sort_values("price", ascending=False).head(10)

        fig2 = px.bar(
            cat_rev, x="price", y="product_category_name", orientation="h",
            text_auto=".2s", title=None, color="price", color_continuous_scale="Teal"
        )
        fig2.update_layout(
            template="plotly_dark", height=400,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="", xaxis_title="Revenue (R$)",
            font=dict(family="Inter, sans-serif", size=12),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig2, use_container_width=True)

        if not cat_rev.empty:
            top_cat = cat_rev.iloc[0]["product_category_name"]
            top_val = cat_rev.iloc[0]["price"]
            st.markdown(f"""
            <div class="insight-box theme-revenue">
                <div class="insight-title">⭐ Category Leader</div>
                <div class="insight-text">
                    <b>{top_cat}</b> leads with <b>R$ {top_val:,.2f}</b> in revenue. This segment should be prioritized for inventory and marketing investment.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ========================================================
    # TAB 2 — ORDERS (Blue Theme) — FIXED PIE CHART
    # ========================================================

    with tab2:
        st.markdown("""
        <div class="section-header">
            <div class="section-header-title"><span style="color:#3b82f6;">📦</span> Order Performance</div>
            <div class="section-header-sub">Analyze order volume and fulfillment metrics</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            monthly_orders = filtered_orders.groupby("order_month")["order_id"].nunique().reset_index()
            fig = px.bar(
                monthly_orders, x="order_month", y="order_id",
                text_auto=True, title=None, color_discrete_sequence=["#3b82f6"]
            )
            fig.update_layout(
                template="plotly_dark", height=350,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title="Month", yaxis_title="Orders",
                font=dict(family="Inter, sans-serif", size=12)
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # FIXED: Group small slices into "Other" for clean pie chart
            status_counts = filtered_orders["order_status"].value_counts().reset_index()
            status_counts.columns = ["status", "count"]
            
            # Group small statuses (< 2%) into Other
            total_status = status_counts["count"].sum()
            status_counts["pct"] = status_counts["count"] / total_status * 100
            
            main_statuses = status_counts[status_counts["pct"] >= 2].copy()
            other_count = status_counts[status_counts["pct"] < 2]["count"].sum()
            
            if other_count > 0:
                other_row = pd.DataFrame([{"status": "Other", "count": other_count, "pct": other_count/total_status*100}])
                main_statuses = pd.concat([main_statuses, other_row], ignore_index=True)
            
            # Sort by count descending
            main_statuses = main_statuses.sort_values("count", ascending=False)
            
            # Custom blue color scale
            blue_colors = ["#1e40af", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe", "#dbeafe"]
            
            fig = px.pie(
                main_statuses, values="count", names="status", hole=0.55,
                title=None, color_discrete_sequence=blue_colors
            )
            fig.update_layout(
                template="plotly_dark", height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=30, b=20),
                font=dict(family="Inter, sans-serif", size=12),
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.15,
                    xanchor="center", x=0.5,
                    font=dict(size=11)
                )
            )
            fig.update_traces(
                textinfo="percent",
                textposition="inside",
                textfont=dict(size=13, color="white", family="Inter, sans-serif"),
                pull=[0.03 if s == "delivered" else 0 for s in main_statuses["status"]],
                marker=dict(line=dict(color="#0f172a", width=2))
            )
            st.plotly_chart(fig, use_container_width=True)

        # Stats Row
        delivered_count = (filtered_orders["order_status"] == "delivered").sum()
        delivery_rate = (delivered_count / total_orders * 100) if total_orders > 0 else 0

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-number" style="color: #3b82f6;">{delivery_rate:.1f}%</div>
                <div class="stat-label">Delivery Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #60a5fa;">{total_orders:,}</div>
                <div class="stat-label">Unique Orders</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #93c5fd;">R$ {aov:,.2f}</div>
                <div class="stat-label">Average Order Value</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-box theme-orders">
            <div class="insight-title">📌 Fulfillment Insight</div>
            <div class="insight-text">
                <b>{delivered_count:,}</b> of <b>{total_orders:,}</b> orders delivered successfully (<b>{delivery_rate:.1f}%</b>). Monitor non-delivered statuses for operational improvements.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # TAB 3 — CUSTOMERS (Violet Theme)
    # ========================================================

    with tab3:
        st.markdown("""
        <div class="section-header">
            <div class="section-header-title"><span style="color:#8b5cf6;">👥</span> Customer Intelligence</div>
            <div class="section-header-sub">Segmentation, retention, and geographic distribution</div>
        </div>
        """, unsafe_allow_html=True)

        orders_with_unique = filtered_orders.merge(customers[["customer_id", "customer_unique_id"]], on="customer_id", how="left")
        cust_orders = orders_with_unique.groupby("customer_unique_id")["order_id"].nunique().reset_index()
        cust_orders.columns = ["customer_unique_id", "order_count"]

        def segment(count):
            if count == 1: return "Low Frequency"
            elif count <= 5: return "Medium Frequency"
            return "High Frequency"

        cust_orders["segment"] = cust_orders["order_count"].apply(segment)
        seg_counts = cust_orders["segment"].value_counts().reset_index()
        seg_counts.columns = ["segment", "count"]

        c1, c2 = st.columns(2)

        with c1:
            fig = px.pie(
                seg_counts, values="count", names="segment", hole=0.55,
                title=None, color_discrete_sequence=["#8b5cf6", "#a78bfa", "#c4b5fd"]
            )
            fig.update_layout(
                template="plotly_dark", height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=30, b=20),
                font=dict(family="Inter, sans-serif", size=12),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
            )
            fig.update_traces(textinfo="percent+label", textfont=dict(size=12))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            state_cust = orders_full.groupby("customer_state")["customer_unique_id"].nunique().reset_index().sort_values("customer_unique_id", ascending=False).head(10)
            fig = px.bar(
                state_cust, x="customer_state", y="customer_unique_id",
                text_auto=True, title=None, color="customer_unique_id", color_continuous_scale="Purples"
            )
            fig.update_layout(
                template="plotly_dark", height=350,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title="State", yaxis_title="Unique Customers",
                font=dict(family="Inter, sans-serif", size=12),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

        repeat_customers = cust_orders[cust_orders["order_count"] > 1]["customer_unique_id"].nunique()
        customer_count = cust_orders["customer_unique_id"].nunique()
        repeat_rate = (repeat_customers / customer_count * 100) if customer_count > 0 else 0

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-number" style="color: #8b5cf6;">{customer_count:,}</div>
                <div class="stat-label">Total Unique Customers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #a78bfa;">{repeat_customers:,}</div>
                <div class="stat-label">Repeat Customers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" style="color: #c4b5fd;">{repeat_rate:.1f}%</div>
                <div class="stat-label">Repeat Purchase Rate</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box theme-customers">
            <div class="insight-title">🎯 Retention Opportunity</div>
            <div class="insight-text">
                High-frequency customers represent the most valuable segment for loyalty programs, while low-frequency segments present the largest re-engagement opportunity.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # TAB 4 — RECOMMENDATIONS (Orange Theme)
    # ========================================================

    with tab4:
        st.markdown("""
        <div class="section-header">
            <div class="section-header-title"><span style="color:#f59e0b;">🤖</span> Recommendation Insights</div>
            <div class="section-header-sub">Cross-selling patterns and category associations</div>
        </div>
        """, unsafe_allow_html=True)

        order_products = order_items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")[["order_id", "product_id", "product_category_name"]]

        @st.cache_data
        def get_product_pairs(data):
            pairs = []
            for order_id, group in data.groupby("order_id"):
                categories = group["product_category_name"].dropna().unique()
                if len(categories) > 1:
                    for i, cat1 in enumerate(categories):
                        for cat2 in categories[i+1:]:
                            if cat1 != cat2:
                                pairs.append((cat1, cat2))
            if not pairs:
                return pd.DataFrame(columns=["category_1", "category_2", "frequency"])
            pairs_df = pd.DataFrame(pairs, columns=["category_1", "category_2"])
            return pairs_df.groupby(["category_1", "category_2"]).size().reset_index(name="frequency").sort_values("frequency", ascending=False).head(15)

        pair_counts = get_product_pairs(order_products)

        if not pair_counts.empty:
            pair_counts["pair"] = pair_counts["category_1"] + " + " + pair_counts["category_2"]
            
            fig = px.bar(
                pair_counts.head(10), x="frequency", y="pair", orientation="h",
                text_auto=True, title=None, color="frequency", color_continuous_scale="YlOrBr"
            )
            fig.update_layout(
                template="plotly_dark", height=400,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis_title="Co-purchase Frequency", yaxis_title="",
                font=dict(family="Inter, sans-serif", size=12),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="section-header" style="margin-top:1rem;">
            <div class="section-header-title"><span style="color:#f59e0b;">🛒</span> Category Order Presence</div>
            <div class="section-header-sub">Most frequently appearing categories across orders</div>
        </div>
        """, unsafe_allow_html=True)

        cross_sell = order_items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        category_orders = cross_sell.groupby("product_category_name")["order_id"].nunique().reset_index()
        category_orders.columns = ["category", "order_count"]
        category_orders = category_orders.sort_values("order_count", ascending=False).head(10)

        fig = px.bar(
            category_orders, x="order_count", y="category", orientation="h",
            text_auto=True, title=None, color="order_count", color_continuous_scale="Oranges"
        )
        fig.update_layout(
            template="plotly_dark", height=380,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="", xaxis_title="Order Presence",
            font=dict(family="Inter, sans-serif", size=12),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box theme-recs">
            <div class="insight-title">🚀 Business Application</div>
            <div class="insight-text">
                Co-purchase patterns enable data-driven product bundling, personalized recommendations, and targeted campaigns to increase basket size and customer lifetime value.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # TAB 5 — SQL SHOWCASE (Indigo Theme)
    # ========================================================

    with tab5:
        st.markdown("""
        <div class="section-header">
            <div class="section-header-title"><span style="color:#6366f1;">🧠</span> SQL Analytics Engine</div>
            <div class="section-header-sub">Query logic powering every metric in this dashboard</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box theme-sql" style="margin-bottom: 1.5rem;">
            <div class="insight-title">🔎 From SQL to Business Insights</div>
            <div class="insight-text">
                Every visualization is validated by structured SQL queries against the Olist relational schema. Below are the core queries calculating the business metrics.
            </div>
        </div>
        """, unsafe_allow_html=True)

        queries = [
            ("💰 Total Payment Revenue", 
             "SELECT\n    ROUND(SUM(payment_value), 2) AS total_revenue\nFROM payments;"),
            ("📅 Monthly Revenue Trend",
             "SELECT\n    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS revenue_month,\n    ROUND(SUM(p.payment_value), 2) AS monthly_revenue\nFROM orders o\nJOIN payments p ON p.order_id = o.order_id\nGROUP BY revenue_month\nORDER BY revenue_month;"),
            ("🏷️ Top Category Revenue",
             "SELECT\n    pr.product_category_name,\n    ROUND(SUM(oi.price), 2) AS category_revenue\nFROM products pr\nJOIN order_items oi ON oi.product_id = pr.product_id\nGROUP BY pr.product_category_name\nORDER BY category_revenue DESC\nLIMIT 10;"),
            ("🗺️ State Revenue Contribution",
             "SELECT\n    c.customer_state,\n    ROUND(SUM(p.payment_value), 2) AS state_revenue\nFROM orders o\nJOIN customers c ON c.customer_id = o.customer_id\nJOIN payments p ON p.order_id = o.order_id\nGROUP BY c.customer_state\nORDER BY state_revenue DESC;"),
            ("📦 Total Order Volume",
             "SELECT\n    COUNT(DISTINCT order_id) AS total_orders\nFROM orders;"),
            ("📊 Monthly Order Trend",
             "SELECT\n    DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS order_month,\n    COUNT(DISTINCT order_id) AS total_orders\nFROM orders\nGROUP BY order_month\nORDER BY order_month;"),
            ("✅ Order Status Breakdown",
             "SELECT\n    order_status,\n    COUNT(*) AS total_orders\nFROM orders\nGROUP BY order_status\nORDER BY total_orders DESC;"),
            ("👥 Unique Customer Count",
             "SELECT\n    COUNT(DISTINCT c.customer_unique_id) AS unique_customers\nFROM orders o\nJOIN customers c ON c.customer_id = o.customer_id;"),
            ("🔄 Repeat Customer Rate",
             "SELECT\n    ROUND(100.0 * SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_customer_rate\nFROM (\n    SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS purchase_count\n    FROM orders o\n    JOIN customers c ON c.customer_id = o.customer_id\n    GROUP BY c.customer_unique_id\n) t;"),
            ("🎯 Customer Segmentation",
             "SELECT\n    CASE\n        WHEN total_orders = 1 THEN 'Low Frequency'\n        WHEN total_orders BETWEEN 2 AND 5 THEN 'Medium Frequency'\n        ELSE 'High Frequency'\n    END AS customer_segment,\n    COUNT(*) AS total_customers\nFROM (\n    SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS total_orders\n    FROM orders o\n    JOIN customers c ON o.customer_id = c.customer_id\n    GROUP BY c.customer_unique_id\n) t\nGROUP BY customer_segment;"),
            ("🏆 Top Customers by Lifetime Value",
             "SELECT\n    c.customer_unique_id,\n    ROUND(SUM(p.payment_value), 2) AS customer_lifetime_revenue\nFROM orders o\nJOIN customers c ON o.customer_id = c.customer_id\nJOIN payments p ON p.order_id = o.order_id\nGROUP BY c.customer_unique_id\nORDER BY customer_lifetime_revenue DESC\nLIMIT 10;")
        ]

        for i in range(0, len(queries), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(queries):
                    title, sql = queries[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="query-card">
                            <div class="query-header">📋 {title}</div>
                            <div class="query-sql">{sql}</div>
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header" style="margin-top:1.5rem;">
            <div class="section-header-title"><span style="color:#6366f1;">📊</span> Dataset Validation</div>
            <div class="section-header-sub">Core entity counts across the entire dataset</div>
        </div>
        """, unsafe_allow_html=True)

        v1, v2, v3 = st.columns(3)
        with v1:
            st.markdown(f"""
            <div class="content-card" style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #818cf8; margin-bottom: 0.3rem;">{products["product_id"].nunique():,}</div>
                <div style="color: #94a3b8; font-weight: 600; font-size: 0.85rem;">Unique Products</div>
            </div>
            """, unsafe_allow_html=True)
        with v2:
            st.markdown(f"""
            <div class="content-card" style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #818cf8; margin-bottom: 0.3rem;">{products["product_category_name"].nunique():,}</div>
                <div style="color: #94a3b8; font-weight: 600; font-size: 0.85rem;">Product Categories</div>
            </div>
            """, unsafe_allow_html=True)
        with v3:
            st.markdown(f"""
            <div class="content-card" style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #818cf8; margin-bottom: 0.3rem;">{customers["customer_unique_id"].nunique():,}</div>
                <div style="color: #94a3b8; font-weight: 600; font-size: 0.85rem;">Unique Customers</div>
            </div>
            """, unsafe_allow_html=True)

    # ========================================================
    # FOOTER — AUTHOR INFO (Redesigned)
    # ========================================================

    st.markdown("""
    <div class="dashboard-footer">
        <div style="display: flex; justify-content: center; align-items: center; gap: 0.6rem; margin-bottom: 0.4rem;">
            <span style="font-size: 1.3rem;">👩‍💻</span>
            <span class="author">Varshini A S</span>
        </div>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.6rem;">
            <span style="background: rgba(16, 185, 129, 0.12); color: #34d399; padding: 0.25rem 0.7rem; border-radius: 100px; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(16, 185, 129, 0.2);">🌟 GSSoC Contributor</span>
            <span style="background: rgba(245, 158, 11, 0.12); color: #fbbf24; padding: 0.25rem 0.7rem; border-radius: 100px; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(245, 158, 11, 0.2);">💼 Open for Internships</span>
            <span style="background: rgba(99, 102, 241, 0.12); color: #818cf8; padding: 0.25rem 0.7rem; border-radius: 100px; font-size: 0.75rem; font-weight: 600; border: 1px solid rgba(99, 102, 241, 0.2);">🚀 Available for Freelancing</span>
        </div>
        <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 0.8rem;">
            Data Analytics · SQL · Python · Streamlit · Business Intelligence
        </div>
        <div style="display: flex; justify-content: center; gap: 1rem;">
            <a href="https://linkedin.com/in/varshini-as" target="_blank" style="color: #94a3b8; text-decoration: none; font-size: 0.8rem; transition: color 0.2s;">LinkedIn</a>
            <span style="color: #334155;">·</span>
            <a href="https://github.com/asvarshini" target="_blank" style="color: #94a3b8; text-decoration: none; font-size: 0.8rem; transition: color 0.2s;">GitHub</a>
            <span style="color: #334155;">·</span>
            <a href="https://asvarshini.github.io" target="_blank" style="color: #94a3b8; text-decoration: none; font-size: 0.8rem; transition: color 0.2s;">Portfolio</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Upload the Olist dataset files into `01_dataset/00_raw_data/` to launch the dashboard.")
