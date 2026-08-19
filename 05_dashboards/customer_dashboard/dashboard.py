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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(99,102,241,0.10), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(14,165,233,0.08), transparent 25%),
            #0b1120;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    p, label {
        color: #cbd5e1;
    }

    /* ---------- HERO ---------- */

    .hero {
        padding: 2.2rem 2.4rem;
        border-radius: 24px;
        margin-bottom: 1.5rem;
        background:
            linear-gradient(
                135deg,
                rgba(79,70,229,0.28),
                rgba(14,165,233,0.18),
                rgba(15,23,42,0.85)
            );
        border: 1px solid rgba(148,163,184,0.16);
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.35rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #cbd5e1;
        margin-bottom: 1.2rem;
    }

    .hero-tag {
        display: inline-block;
        padding: 0.45rem 0.8rem;
        margin-right: 0.45rem;
        border-radius: 999px;
        background: rgba(99,102,241,0.18);
        border: 1px solid rgba(129,140,248,0.25);
        color: #c7d2fe;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* ---------- KPI CARDS ---------- */

    .metric-card {
        padding: 1.15rem 1.2rem;
        min-height: 125px;
        border-radius: 18px;
        background: rgba(15,23,42,0.78);
        border: 1px solid rgba(148,163,184,0.14);
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    .metric-label {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #f8fafc;
    }

    .metric-description {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.35rem;
    }

    /* ---------- SECTION HEADER ---------- */

    .section-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #f8fafc;
        margin-top: 1rem;
        margin-bottom: 0.25rem;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-bottom: 1rem;
    }

    /* ---------- INSIGHT CARDS ---------- */

    .insight {
        padding: 1.15rem 1.3rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(148,163,184,0.13);
    }

    .insight-purple {
        border-left: 4px solid #8b5cf6;
    }

    .insight-blue {
        border-left: 4px solid #38bdf8;
    }

    .insight-green {
        border-left: 4px solid #34d399;
    }

    .insight-orange {
        border-left: 4px solid #f59e0b;
    }

    .insight-title {
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.35rem;
    }

    .insight-text {
        color: #cbd5e1;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    /* ---------- HIGHLIGHT BOX ---------- */

    .highlight-box {
        padding: 1.4rem;
        border-radius: 20px;
        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.14),
                rgba(14,165,233,0.08)
            );
        border: 1px solid rgba(129,140,248,0.18);
        margin: 1rem 0;
    }

    .highlight-number {
        font-size: 2rem;
        font-weight: 800;
        color: #a5b4fc;
    }

    .highlight-label {
        color: #cbd5e1;
        font-size: 0.85rem;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid rgba(148,163,184,0.12);
    }

    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        margin-top: 3rem;
        padding: 1.5rem;
        text-align: center;
        border-top: 1px solid rgba(148,163,184,0.12);
        color: #64748b;
        font-size: 0.82rem;
    }

    /* ---------- TAB ---------- */

    button[data-baseweb="tab"] {
        font-weight: 650;
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

        if os.path.exists(local_path):
            return local_path

        return cloud_path

    orders = pd.read_csv(
        get_data_path("olist_orders_dataset.csv")
    )

    order_items = pd.read_csv(
        get_data_path("olist_order_items_dataset.csv")
    )

    payments = pd.read_csv(
        get_data_path("olist_order_payments_dataset.csv")
    )

    customers = pd.read_csv(
        get_data_path("olist_customers_dataset.csv")
    )

    products = pd.read_csv(
        get_data_path("olist_products_dataset.csv")
    )

    # Dates
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    orders["order_month"] = (
        orders["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    return orders, order_items, payments, customers, products


# ============================================================
# LOAD DATA
# ============================================================

try:

    orders, order_items, payments, customers, products = load_data()

    data_loaded = True

except Exception as e:

    st.error(f"Error loading data: {e}")
    st.info(
        "Make sure the Olist CSV files are available inside "
        "01_dataset/00_raw_data/"
    )

    data_loaded = False


# ============================================================
# MAIN APPLICATION
# ============================================================

if data_loaded:

    # ========================================================
    # HERO
    # ========================================================

    st.markdown("""
    <div class="hero">

        <div class="hero-title">
            📊 Olist Business Analytics Suite
        </div>

        <div class="hero-subtitle">
            End-to-end business intelligence analysis of Brazilian
            e-commerce performance using SQL, Python and Streamlit.
        </div>

        <span class="hero-tag">100K+ Orders</span>
        <span class="hero-tag">SQL Analytics</span>
        <span class="hero-tag">Customer Intelligence</span>
        <span class="hero-tag">Revenue Analytics</span>
        <span class="hero-tag">Interactive Dashboard</span>

    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.markdown("""
    <div class="sidebar-title">
        🔍 Dashboard Filters
    </div>

    <div class="sidebar-subtitle">
        Explore business performance dynamically
    </div>
    """, unsafe_allow_html=True)

    min_date = orders["order_purchase_timestamp"].min().date()
    max_date = orders["order_purchase_timestamp"].max().date()

    date_range = st.sidebar.date_input(
        "Purchase Date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    states = (
        ["All"]
        + sorted(
            customers["customer_state"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_state = st.sidebar.selectbox(
        "Customer State",
        states
    )

    # Handle date selection safely
    if len(date_range) == 2:

        start_date = pd.Timestamp(date_range[0])
        end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    else:

        start_date = pd.Timestamp(min_date)
        end_date = pd.Timestamp(max_date) + pd.Timedelta(days=1)


    # ========================================================
    # FILTER ORDERS
    # ========================================================

    mask = (
        (orders["order_purchase_timestamp"] >= start_date)
        &
        (orders["order_purchase_timestamp"] < end_date)
    )

    filtered_orders = orders.loc[mask].copy()

    # State filter
    if selected_state != "All":

        state_customer_ids = customers.loc[
            customers["customer_state"] == selected_state,
            "customer_id"
        ]

        filtered_orders = filtered_orders[
            filtered_orders["customer_id"].isin(
                state_customer_ids
            )
        ]


    # ========================================================
    # MERGED DATA
    # ========================================================

    orders_with_payments = filtered_orders.merge(
        payments,
        on="order_id",
        how="left"
    )

    orders_with_items = filtered_orders.merge(
        order_items,
        on="order_id",
        how="left"
    )

    orders_full = filtered_orders.merge(
        customers,
        on="customer_id",
        how="left"
    )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_revenue = orders_with_payments[
        "payment_value"
    ].sum()

    total_orders = filtered_orders[
        "order_id"
    ].nunique()

    order_payment_totals = (
        orders_with_payments
        .groupby("order_id")["payment_value"]
        .sum()
    )

    aov = order_payment_totals.mean()

    filtered_customer_ids = (
        filtered_orders["customer_id"]
        .dropna()
        .unique()
    )

    total_customers = customers[
        customers["customer_id"].isin(
            filtered_customer_ids
        )
    ]["customer_unique_id"].nunique()

    # IMPORTANT:
    # This is UNIQUE PRODUCTS, not categories.
    total_products = orders_with_items[
        "product_id"
    ].nunique()

    total_categories = products[
        "product_category_name"
    ].nunique()


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.markdown(
        '<div class="section-title">Business Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Key performance indicators based on the selected filters.'
        '</div>',
        unsafe_allow_html=True
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Total Revenue</div>
            <div class="metric-value">R$ {total_revenue:,.0f}</div>
            <div class="metric-description">
                Payment value
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📦 Orders</div>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-description">
                Unique order IDs
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📈 Average Order Value</div>
            <div class="metric-value">R$ {aov:,.2f}</div>
            <div class="metric-description">
                Average payment per order
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">👥 Unique Customers</div>
            <div class="metric-value">{total_customers:,}</div>
            <div class="metric-description">
                customer_unique_id
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k5:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🛍️ Unique Products</div>
            <div class="metric-value">{total_products:,}</div>
            <div class="metric-description">
                Across {total_categories} categories
            </div>
        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Revenue",
        "📦 Orders",
        "👥 Customers",
        "🤖 Recommendations",
        "🧠 SQL Showcase"
    ])


    # ========================================================
    # TAB 1 — REVENUE
    # ========================================================

    with tab1:

        st.markdown(
            '<div class="section-title">'
            '💰 Revenue Performance'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Understand revenue trends, product-category performance '
            'and geographic contribution.'
            '</div>',
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # Revenue summary
        # ----------------------------------------------------

        monthly_rev = (
            orders_with_payments
            .groupby("order_month")["payment_value"]
            .sum()
            .reset_index()
        )

        fig = px.area(
            monthly_rev,
            x="order_month",
            y="payment_value",
            markers=True,
            title="Monthly Payment Revenue"
        )

        fig.update_layout(
            template="plotly_dark",
            height=430,
            xaxis_title="Month",
            yaxis_title="Revenue (R$)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ----------------------------------------------------
        # Category revenue
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🏷️ Top Product Categories'
            '</div>',
            unsafe_allow_html=True
        )

        items_prod = orders_with_items.merge(
            products[
                [
                    "product_id",
                    "product_category_name"
                ]
            ],
            on="product_id",
            how="left"
        )

        cat_rev = (
            items_prod
            .groupby("product_category_name")["price"]
            .sum()
            .reset_index()
            .sort_values(
                "price",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            cat_rev,
            x="price",
            y="product_category_name",
            orientation="h",
            text_auto=".2s",
            title="Top 10 Categories by Product-Item Revenue"
        )

        fig.update_layout(
            template="plotly_dark",
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="",
            xaxis_title="Product Revenue (R$)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # Business insight
        # ----------------------------------------------------

        if not cat_rev.empty:

            top_category = cat_rev.iloc[0]["product_category_name"]
            top_category_value = cat_rev.iloc[0]["price"]

            st.markdown(f"""
            <div class="insight insight-purple">

                <div class="insight-title">
                    ⭐ Category Leader
                </div>

                <div class="insight-text">
                    <b>{top_category}</b> is the highest-performing
                    category by product-item revenue in the selected
                    dataset, generating approximately
                    <b>R$ {top_category_value:,.2f}</b>.
                </div>

            </div>
            """, unsafe_allow_html=True)


    # ========================================================
    # TAB 2 — ORDERS
    # ========================================================

    with tab2:

        st.markdown(
            '<div class="section-title">'
            '📦 Order Performance'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Explore order volume, purchasing patterns and order status.'
            '</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        # ----------------------------------------------------
        # Monthly orders
        # ----------------------------------------------------

        with c1:

            monthly_orders = (
                filtered_orders
                .groupby("order_month")["order_id"]
                .nunique()
                .reset_index()
            )

            fig = px.bar(
                monthly_orders,
                x="order_month",
                y="order_id",
                title="Monthly Order Volume",
                text_auto=True
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Month",
                yaxis_title="Orders"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        with c2:

            status_counts = (
                filtered_orders["order_status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "status",
                "count"
            ]

            fig = px.pie(
                status_counts,
                values="count",
                names="status",
                hole=0.48,
                title="Order Status Distribution"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # Order statistics
        # ----------------------------------------------------

        delivered_count = (
            filtered_orders["order_status"]
            == "delivered"
        ).sum()

        delivery_rate = (
            delivered_count / total_orders * 100
            if total_orders > 0
            else 0
        )

        d1, d2, d3 = st.columns(3)

        with d1:

            st.markdown(f"""
            <div class="highlight-box">

                <div class="highlight-number">
                    {delivery_rate:.2f}%
                </div>

                <div class="highlight-label">
                    Orders delivered
                </div>

            </div>
            """, unsafe_allow_html=True)

        with d2:

            st.markdown(f"""
            <div class="highlight-box">

                <div class="highlight-number">
                    {total_orders:,}
                </div>

                <div class="highlight-label">
                    Unique orders
                </div>

            </div>
            """, unsafe_allow_html=True)

        with d3:

            st.markdown(f"""
            <div class="highlight-box">

                <div class="highlight-number">
                    R$ {aov:,.2f}
                </div>

                <div class="highlight-label">
                    Payment-based AOV
                </div>

            </div>
            """, unsafe_allow_html=True)


        st.markdown(f"""
        <div class="insight insight-blue">

            <div class="insight-title">
                📌 Order Performance Insight
            </div>

            <div class="insight-text">
                The selected period contains
                <b>{total_orders:,}</b> unique orders.
                Approximately <b>{delivery_rate:.2f}%</b>
                of these orders are marked as delivered.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # TAB 3 — CUSTOMERS
    # ========================================================

    with tab3:

        st.markdown(
            '<div class="section-title">'
            '👥 Customer Intelligence'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Understand customer frequency, retention patterns '
            'and geographic distribution.'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # Customer orders
        # ----------------------------------------------------

        orders_with_unique = filtered_orders.merge(
            customers[
                [
                    "customer_id",
                    "customer_unique_id"
                ]
            ],
            on="customer_id",
            how="left"
        )

        cust_orders = (
            orders_with_unique
            .groupby(
                "customer_unique_id"
            )["order_id"]
            .nunique()
            .reset_index()
        )

        cust_orders.columns = [
            "customer_unique_id",
            "order_count"
        ]


        # ----------------------------------------------------
        # Segmentation
        # ----------------------------------------------------

        def segment(count):

            if count == 1:
                return "Low Frequency"

            elif count <= 5:
                return "Medium Frequency"

            return "High Frequency"


        cust_orders["segment"] = (
            cust_orders["order_count"]
            .apply(segment)
        )


        seg_counts = (
            cust_orders["segment"]
            .value_counts()
            .reset_index()
        )

        seg_counts.columns = [
            "segment",
            "count"
        ]


        c1, c2 = st.columns(2)


        # ----------------------------------------------------
        # Segmentation chart
        # ----------------------------------------------------

        with c1:

            fig = px.pie(
                seg_counts,
                values="count",
                names="segment",
                hole=0.48,
                title="Customer Purchase Frequency"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # State customers
        # ----------------------------------------------------

        with c2:

            state_cust = (
                orders_full
                .groupby("customer_state")
                ["customer_unique_id"]
                .nunique()
                .reset_index()
                .sort_values(
                    "customer_unique_id",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                state_cust,
                x="customer_state",
                y="customer_unique_id",
                text_auto=True,
                title="Top 10 States by Unique Customers"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="State",
                yaxis_title="Unique Customers"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # Customer frequency KPIs
        # ----------------------------------------------------

        repeat_customers = (
            cust_orders[
                cust_orders["order_count"] > 1
            ]
            ["customer_unique_id"]
            .nunique()
        )

        customer_count = (
            cust_orders["customer_unique_id"]
            .nunique()
        )

        repeat_rate = (
            repeat_customers / customer_count * 100
            if customer_count > 0
            else 0
        )


        r1, r2, r3 = st.columns(3)


        with r1:

            st.markdown(f"""
            <div class="highlight-box">

                <div class="highlight-number">
                    {customer_count:,}
                </div>

                <div class="highlight-label">
                    Unique customers
                </div>

            </div>
            """, unsafe_allow_html=True)


        with r2:

            st.markdown(f"""
            <div class="highlight-box">

                <div class="highlight-number">
                    {repeat_customers:,}
                </div>

                <div class="highlight-label">
                    Repeat customers
                </div>

            </div>
            """, unsafe_allow_html=True)


        with r3:

            st.markdown(f"""
            <div class="highlight-box">

                <div class="highlight-number">
                    {repeat_rate:.2f}%
                </div>

                <div class="highlight-label">
                    Repeat customer rate
                </div>

            </div>
            """, unsafe_allow_html=True)


        st.markdown("""
        <div class="insight insight-green">

            <div class="insight-title">
                🎯 Customer Retention Opportunity
            </div>

            <div class="insight-text">
                Customer frequency analysis separates one-time
                purchasers from medium- and high-frequency customers.
                This provides a clear foundation for retention,
                loyalty and re-engagement strategies.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # TAB 4 — RECOMMENDATIONS
    # ========================================================

    with tab4:

        st.markdown(
            '<div class="section-title">'
            '🤖 Product Recommendation Insights'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Discover category combinations and cross-selling opportunities.'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # Product pairs
        # ----------------------------------------------------

        order_products = order_items.merge(
            products[
                [
                    "product_id",
                    "product_category_name"
                ]
            ],
            on="product_id",
            how="left"
        )[
            [
                "order_id",
                "product_id",
                "product_category_name"
            ]
        ]


        @st.cache_data
        def get_product_pairs(data):

            pairs = []

            for order_id, group in data.groupby(
                "order_id"
            ):

                categories = (
                    group[
                        "product_category_name"
                    ]
                    .dropna()
                    .unique()
                )

                if len(categories) > 1:

                    for i, cat1 in enumerate(categories):

                        for cat2 in categories[i + 1:]:

                            if cat1 != cat2:

                                pairs.append(
                                    (
                                        cat1,
                                        cat2
                                    )
                                )

            if not pairs:
                return pd.DataFrame(
                    columns=[
                        "category_1",
                        "category_2",
                        "frequency"
                    ]
                )

            pairs_df = pd.DataFrame(
                pairs,
                columns=[
                    "category_1",
                    "category_2"
                ]
            )

            pair_counts = (
                pairs_df
                .groupby(
                    [
                        "category_1",
                        "category_2"
                    ]
                )
                .size()
                .reset_index(
                    name="frequency"
                )
                .sort_values(
                    "frequency",
                    ascending=False
                )
                .head(15)
            )

            return pair_counts


        pair_counts = get_product_pairs(
            order_products
        )


        if not pair_counts.empty:

            pair_counts["pair"] = (
                pair_counts["category_1"]
                + " + "
                + pair_counts["category_2"]
            )

            fig = px.bar(
                pair_counts.head(10),
                x="frequency",
                y="pair",
                orientation="h",
                text_auto=True,
                title="Top Category Combinations Bought Together"
            )

            fig.update_layout(
                template="plotly_dark",
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Co-purchase Frequency",
                yaxis_title=""
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough multi-category orders for this analysis."
            )


        # ----------------------------------------------------
        # Cross-category
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🛒 Cross-Category Buying Patterns'
            '</div>',
            unsafe_allow_html=True
        )


        cross_sell = order_items.merge(
            products[
                [
                    "product_id",
                    "product_category_name"
                ]
            ],
            on="product_id",
            how="left"
        )


        category_orders = (
            cross_sell
            .groupby(
                "product_category_name"
            )["order_id"]
            .nunique()
            .reset_index()
        )

        category_orders.columns = [
            "category",
            "order_count"
        ]

        category_orders = (
            category_orders
            .sort_values(
                "order_count",
                ascending=False
            )
            .head(10)
        )


        fig = px.bar(
            category_orders,
            x="order_count",
            y="category",
            orientation="h",
            text_auto=True,
            title="Categories with Highest Order Presence"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ----------------------------------------------------
        # Recommendation demo
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '💡 Recommendation Explorer'
            '</div>',
            unsafe_allow_html=True
        )


        top_categories = (
            products[
                "product_category_name"
            ]
            .dropna()
            .value_counts()
            .head(20)
            .index
            .tolist()
        )


        if top_categories:

            selected_category = st.selectbox(
                "Choose a category",
                top_categories
            )


            if not pair_counts.empty:

                related_pairs = pair_counts[
                    (
                        pair_counts["category_1"]
                        == selected_category
                    )
                    |
                    (
                        pair_counts["category_2"]
                        == selected_category
                    )
                ].head(5)


                if not related_pairs.empty:

                    for _, row in related_pairs.iterrows():

                        if (
                            row["category_1"]
                            == selected_category
                        ):

                            recommended = row[
                                "category_2"
                            ]

                        else:

                            recommended = row[
                                "category_1"
                            ]


                        st.markdown(f"""
                        <div class="insight insight-orange">

                            <div class="insight-title">
                                🛍️ Customers who bought
                                {selected_category}
                            </div>

                            <div class="insight-text">
                                Consider recommending
                                <b>{recommended}</b>
                                based on observed
                                co-purchase behaviour.
                            </div>

                        </div>
                        """, unsafe_allow_html=True)

                else:

                    st.info(
                        "No strong category association found."
                    )


        st.markdown("""
        <div class="insight insight-purple">

            <div class="insight-title">
                🚀 Business Application
            </div>

            <div class="insight-text">
                These patterns can support product bundling,
                cross-selling, recommendation systems and
                targeted marketing campaigns.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # TAB 5 — SQL SHOWCASE
    # ========================================================

    with tab5:

        st.markdown(
            '<div class="section-title">'
            '🧠 SQL Analytics Showcase'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'Selected SQL logic used to validate and calculate '
            'the business metrics presented in this dashboard.'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # Revenue
        # ----------------------------------------------------

        st.subheader("💰 Revenue Analysis")


        with st.expander(
            "KPI 1 — Total Payment Revenue"
        ):

            st.code("""
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;
            """, language="sql")


        with st.expander(
            "KPI 2 — Monthly Revenue"
        ):

            st.code("""
SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS revenue_month,
    ROUND(
        SUM(p.payment_value),
        2
    ) AS monthly_revenue
FROM orders o
JOIN payments p
    ON p.order_id = o.order_id
GROUP BY revenue_month
ORDER BY revenue_month;
            """, language="sql")


        with st.expander(
            "KPI 3 — Product Category Revenue"
        ):

            st.code("""
SELECT
    pr.product_category_name,
    ROUND(
        SUM(oi.price),
        2
    ) AS category_revenue
FROM products pr
JOIN order_items oi
    ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name
ORDER BY category_revenue DESC
LIMIT 10;
            """, language="sql")


        with st.expander(
            "KPI 4 — State Revenue Contribution"
        ):

            st.code("""
SELECT
    c.customer_state,
    ROUND(
        SUM(p.payment_value),
        2
    ) AS state_revenue
FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id
JOIN payments p
    ON p.order_id = o.order_id
GROUP BY c.customer_state
ORDER BY state_revenue DESC;
            """, language="sql")


        # ----------------------------------------------------
        # Orders
        # ----------------------------------------------------

        st.subheader("📦 Order Analysis")


        with st.expander(
            "KPI 5 — Total Orders"
        ):

            st.code("""
SELECT
    COUNT(DISTINCT order_id)
    AS total_orders
FROM orders;
            """, language="sql")


        with st.expander(
            "KPI 6 — Monthly Order Trend"
        ):

            st.code("""
SELECT
    DATE_FORMAT(
        order_purchase_timestamp,
        '%Y-%m'
    ) AS order_month,
    COUNT(DISTINCT order_id)
    AS total_orders
FROM orders
GROUP BY order_month
ORDER BY order_month;
            """, language="sql")


        with st.expander(
            "KPI 7 — Order Status Distribution"
        ):

            st.code("""
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
            """, language="sql")


        # ----------------------------------------------------
        # Customers
        # ----------------------------------------------------

        st.subheader("👥 Customer Analysis")


        with st.expander(
            "KPI 8 — Unique Customers"
        ):

            st.code("""
SELECT
    COUNT(DISTINCT c.customer_unique_id)
    AS unique_customers
FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id;
            """, language="sql")


        with st.expander(
            "KPI 9 — Repeat Customer Rate"
        ):

            st.code("""
SELECT
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
    ) AS repeat_customer_rate
FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id)
        AS purchase_count
    FROM orders o
    JOIN customers c
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
) t;
            """, language="sql")


        with st.expander(
            "KPI 10 — Customer Segmentation"
        ):

            st.code("""
SELECT
    CASE
        WHEN total_orders = 1
            THEN 'Low Frequency'

        WHEN total_orders BETWEEN 2 AND 5
            THEN 'Medium Frequency'

        ELSE 'High Frequency'
    END AS customer_segment,

    COUNT(*) AS total_customers

FROM (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id)
        AS total_orders

    FROM orders o

    JOIN customers c
        ON o.customer_id = c.customer_id

    GROUP BY c.customer_unique_id
) t

GROUP BY customer_segment;
            """, language="sql")


        with st.expander(
            "KPI 11 — Top Customers by Lifetime Revenue"
        ):

            st.code("""
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
            """, language="sql")


        # ----------------------------------------------------
        # DATASET METRICS
        # ----------------------------------------------------

        st.subheader("📊 Dataset Validation Metrics")


        v1, v2, v3 = st.columns(3)


        with v1:

            st.markdown(f"""
            <div class="metric-card">

                <div class="metric-label">
                    🛍️ Unique Products
                </div>

                <div class="metric-value">
                    {products["product_id"].nunique():,}
                </div>

                <div class="metric-description">
                    Distinct product IDs
                </div>

            </div>
            """, unsafe_allow_html=True)


        with v2:

            st.markdown(f"""
            <div class="metric-card">

                <div class="metric-label">
                    🏷️ Product Categories
                </div>

                <div class="metric-value">
                    {products["product_category_name"].nunique():,}
                </div>

                <div class="metric-description">
                    Distinct category values
                </div>

            </div>
            """, unsafe_allow_html=True)


        with v3:

            st.markdown(f"""
            <div class="metric-card">

                <div class="metric-label">
                    👥 Unique Customers
                </div>

                <div class="metric-value">
                    {customers["customer_unique_id"].nunique():,}
                </div>

                <div class="metric-description">
                    customer_unique_id
                </div>

            </div>
            """, unsafe_allow_html=True)


        st.markdown("""
        <div class="insight insight-blue">

            <div class="insight-title">
                🔎 Why these metrics matter
            </div>

            <div class="insight-text">
                The dashboard distinguishes between orders,
                customer records, actual unique customers,
                product IDs and product categories. This prevents
                different business entities from being incorrectly
                treated as the same metric.
            </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("""
    <div class="footer">

        <div>
            <b>Olist Business Analytics Suite</b>
        </div>

        <div>
            Built by Varshini A S
            · SQL · Python · Streamlit · Plotly
        </div>

        <div>
            Business Intelligence & Data Analytics Portfolio Project
        </div>

    </div>
    """, unsafe_allow_html=True)


else:

    st.info(
        "Upload the Olist dataset files into "
        "01_dataset/00_raw_data/ to start the dashboard."
    )
