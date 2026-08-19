import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Olist Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 50%,
            #0f172a 100%
        );
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #0f172a 100%
        );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    /* Main title */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.8rem;
    }

    /* Section titles */
    .section-title {
        color: #f8fafc;
        font-size: 1.55rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.95)
        );
        border: 1px solid rgba(148,163,184,0.15);
        border-radius: 18px;
        padding: 1.25rem;
        min-height: 145px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.18);
        transition: transform 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99,102,241,0.45);
    }

    .kpi-icon {
        font-size: 1.5rem;
    }

    .kpi-label {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 1.7rem;
        font-weight: 750;
        margin-top: 0.25rem;
    }

    .kpi-note {
        color: #64748b;
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }

    /* Insight cards */
    .insight-card {
        background: linear-gradient(
            135deg,
            rgba(99,102,241,0.12),
            rgba(6,182,212,0.08)
        );
        border: 1px solid rgba(99,102,241,0.22);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .insight-title {
        color: #a5b4fc;
        font-weight: 700;
        font-size: 1rem;
    }

    .insight-text {
        color: #cbd5e1;
        margin-top: 0.4rem;
        line-height: 1.55;
    }

    /* Footer */
    .footer {
        margin-top: 3rem;
        padding: 1.5rem;
        text-align: center;
        border-top: 1px solid rgba(148,163,184,0.12);
        color: #64748b;
    }

    .footer strong {
        color: #94a3b8;
    }

    /* Analysis approach */
    .approach-card {
        background: linear-gradient(
            135deg,
            rgba(15,23,42,0.96),
            rgba(30,41,59,0.96)
        );
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 18px;
        padding: 1.6rem;
        margin-top: 1.5rem;
    }

    .approach-step {
        background: rgba(255,255,255,0.025);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.45rem 0;
        color: #cbd5e1;
    }

    .step-number {
        color: #818cf8;
        font-weight: 700;
        margin-right: 0.5rem;
    }

    /* Hide Streamlit menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero-title">
    📊 Olist E-Commerce Intelligence
</div>

<div class="hero-subtitle">
    From raw transactions to actionable business insights —
    SQL • Python • Streamlit • Plotly
</div>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
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

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    orders["order_estimated_delivery_date"] = pd.to_datetime(
        orders["order_estimated_delivery_date"]
    )

    orders["order_month"] = (
        orders["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    return orders, order_items, payments, customers, products


try:

    orders, order_items, payments, customers, products = load_data()

    data_loaded = True

except Exception as e:

    st.error(f"❌ Error loading data: {e}")

    st.info(
        "Make sure the Olist CSV files are available in "
        "`01_dataset/00_raw_data/`."
    )

    data_loaded = False


# ============================================================
# DASHBOARD
# ============================================================

if data_loaded:

    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.markdown(
        "## 🔍 Dashboard Filters"
    )

    st.sidebar.caption(
        "Filter the analysis by purchase date and customer state."
    )

    min_date = orders[
        "order_purchase_timestamp"
    ].min().date()

    max_date = orders[
        "order_purchase_timestamp"
    ].max().date()

    date_range = st.sidebar.date_input(
        "📅 Purchase Date Range",
        value=[min_date, max_date],
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
        "📍 Customer State",
        states
    )

    # ========================================================
    # FILTER DATA
    # ========================================================

    mask = (
        orders["order_purchase_timestamp"]
        >= pd.Timestamp(date_range[0])
    ) & (
        orders["order_purchase_timestamp"]
        <= pd.Timestamp(date_range[1])
    )

    filtered_orders = orders[mask].copy()

    if selected_state != "All":

        state_customer_ids = customers[
            customers["customer_state"] == selected_state
        ]["customer_id"]

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

    total_payment_value = (
        orders_with_payments["payment_value"]
        .sum()
    )

    total_orders = (
        filtered_orders["order_id"]
        .nunique()
    )

    order_payment_totals = (
        orders_with_payments
        .groupby("order_id")["payment_value"]
        .sum()
    )

    aov = (
        order_payment_totals.mean()
        if len(order_payment_totals) > 0
        else 0
    )

    filtered_customer_ids = (
        filtered_orders["customer_id"]
        .dropna()
        .unique()
    )

    total_customers = (
        customers[
            customers["customer_id"]
            .isin(filtered_customer_ids)
        ]["customer_unique_id"]
        .nunique()
    )

    unique_products = (
        orders_with_items["product_id"]
        .nunique()
    )

    # ========================================================
    # KPI HEADER
    # ========================================================

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">💰</div>
                <div class="kpi-label">Payment Value</div>
                <div class="kpi-value">R$ {total_payment_value:,.0f}</div>
                <div class="kpi-note">Sum of recorded payments</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">📦</div>
                <div class="kpi-label">Orders</div>
                <div class="kpi-value">{total_orders:,}</div>
                <div class="kpi-note">Distinct order IDs</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">📈</div>
                <div class="kpi-label">AOV</div>
                <div class="kpi-value">R$ {aov:,.0f}</div>
                <div class="kpi-note">Average payment per order</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-label">Unique Customers</div>
                <div class="kpi-value">{total_customers:,}</div>
                <div class="kpi-note">customer_unique_id</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k5:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">🛍️</div>
                <div class="kpi-label">Unique Products</div>
                <div class="kpi-value">{unique_products:,}</div>
                <div class="kpi-note">Distinct product IDs</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # TABS
    # ========================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📈 Revenue",
            "📦 Orders",
            "👥 Customers",
            "🤖 Recommendations",
            "📝 SQL Showcase"
        ]
    )

    # ========================================================
    # TAB 1 — REVENUE
    # ========================================================

    with tab1:

        st.markdown(
            '<div class="section-title">💰 Revenue & Product Performance</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Monthly Payment Value
        # ----------------------------------------------------

        with col1:

            monthly_payment = (
                orders_with_payments
                .groupby("order_month")["payment_value"]
                .sum()
                .reset_index()
            )

            fig = px.area(
                monthly_payment,
                x="order_month",
                y="payment_value",
                markers=True,
                title="Monthly Payment Value"
            )

            fig.update_layout(
                template="plotly_dark",
                height=430,
                xaxis_title="Purchase Month",
                yaxis_title="Payment Value (R$)",
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Top Categories
        # ----------------------------------------------------

        with col2:

            items_products = orders_with_items.merge(
                products[
                    [
                        "product_id",
                        "product_category_name"
                    ]
                ],
                on="product_id",
                how="left"
            )

            category_revenue = (
                items_products
                .groupby("product_category_name")["price"]
                .sum()
                .reset_index()
                .sort_values(
                    "price",
                    ascending=False
                )
                .head(10)
            )

            category_revenue = category_revenue.dropna()

            fig = px.bar(
                category_revenue,
                x="price",
                y="product_category_name",
                orientation="h",
                title="Top 10 Categories by Product-Item Value",
                labels={
                    "price": "Product-Item Value (R$)",
                    "product_category_name": "Category"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=430,
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Revenue Insights
        # ----------------------------------------------------

        top_category = (
            category_revenue.iloc[0]
            if not category_revenue.empty
            else None
        )

        if top_category is not None:

            category_share = (
                top_category["price"]
                / total_payment_value
                * 100
                if total_payment_value > 0
                else 0
            )

            st.markdown(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        💡 Revenue Insight
                    </div>

                    <div class="insight-text">
                        <strong>{top_category["product_category_name"]}</strong>
                        is the highest-performing product category
                        by product-item value, generating
                        <strong>
                            R$ {top_category["price"]:,.2f}
                        </strong>.
                        This represents approximately
                        <strong>{category_share:.2f}%</strong>
                        of total recorded payment value.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # State Revenue
        # ----------------------------------------------------

        state_payment = (
            orders_full
            .merge(
                payments,
                on="order_id",
                how="left"
            )
            .groupby("customer_state")["payment_value"]
            .sum()
            .reset_index()
            .sort_values(
                "payment_value",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            state_payment,
            x="customer_state",
            y="payment_value",
            title="Top 10 States by Payment Value",
            labels={
                "customer_state": "State",
                "payment_value": "Payment Value (R$)"
            }
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ========================================================
    # TAB 2 — ORDERS
    # ========================================================

    with tab2:

        st.markdown(
            '<div class="section-title">📦 Order Performance</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Monthly Orders
        # ----------------------------------------------------

        with col1:

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
                labels={
                    "order_month": "Purchase Month",
                    "order_id": "Orders"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        with col2:

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
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Delivery status insight
        # ----------------------------------------------------

        delivered = (
            filtered_orders[
                filtered_orders["order_status"]
                == "delivered"
            ]["order_id"]
            .nunique()
        )

        delivery_rate = (
            delivered / total_orders * 100
            if total_orders > 0
            else 0
        )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    🚚 Delivery Performance
                </div>

                <div class="insight-text">
                    <strong>{delivered:,}</strong>
                    orders were delivered,
                    representing a
                    <strong>{delivery_rate:.2f}%</strong>
                    delivery-status share among the
                    currently filtered orders.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # TAB 3 — CUSTOMERS
    # ========================================================

    with tab3:

        st.markdown(
            '<div class="section-title">👥 Customer Intelligence</div>',
            unsafe_allow_html=True
        )

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

        customer_orders = (
            orders_with_unique
            .groupby(
                "customer_unique_id"
            )["order_id"]
            .nunique()
            .reset_index()
        )

        customer_orders.columns = [
            "customer_unique_id",
            "order_count"
        ]

        def segment(count):

            if count == 1:
                return "Low Frequency"

            elif count <= 5:
                return "Medium Frequency"

            else:
                return "High Frequency"

        customer_orders["segment"] = (
            customer_orders["order_count"]
            .apply(segment)
        )

        segment_counts = (
            customer_orders["segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = [
            "segment",
            "count"
        ]

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Segmentation
        # ----------------------------------------------------

        with col1:

            fig = px.pie(
                segment_counts,
                values="count",
                names="segment",
                hole=0.48,
                title="Customer Purchase Frequency"
            )

            fig.update_layout(
                template="plotly_dark",
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Customers by State
        # ----------------------------------------------------

        with col2:

            state_customers = (
                orders_full
                .groupby(
                    "customer_state"
                )["customer_unique_id"]
                .nunique()
                .reset_index()
                .sort_values(
                    "customer_unique_id",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                state_customers,
                x="customer_state",
                y="customer_unique_id",
                title="Top 10 States by Unique Customers",
                labels={
                    "customer_state": "State",
                    "customer_unique_id":
                        "Unique Customers"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Repeat customer calculation
        # ----------------------------------------------------

        total_customer_count = len(
            customer_orders
        )

        repeat_customer_count = (
            customer_orders[
                customer_orders["order_count"] > 1
            ].shape[0]
        )

        repeat_rate = (
            repeat_customer_count
            / total_customer_count
            * 100
            if total_customer_count > 0
            else 0
        )

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-title">
                    🔁 Customer Retention Insight
                </div>

                <div class="insight-text">
                    <strong>{repeat_customer_count:,}</strong>
                    customers placed more than one order,
                    giving a repeat-customer rate of
                    <strong>{repeat_rate:.2f}%</strong>.
                    This highlights an opportunity to improve
                    customer retention and repeat purchasing.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # Segment table
        # ----------------------------------------------------

        display_segments = segment_counts.copy()

        display_segments["percentage"] = (
            display_segments["count"]
            / display_segments["count"].sum()
            * 100
        )

        display_segments["percentage"] = (
            display_segments["percentage"]
            .round(2)
        )

        display_segments.columns = [
            "Customer Segment",
            "Customers",
            "Share (%)"
        ]

        st.subheader("Customer Segment Breakdown")

        st.dataframe(
            display_segments,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # TAB 4 — RECOMMENDATIONS
    # ========================================================

    with tab4:

        st.markdown(
            '<div class="section-title">🤖 Product Association Analysis</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Category-level co-purchase analysis based on products "
            "appearing together in the same order."
        )

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
                    .tolist()
                )

                if len(categories) > 1:

                    for i in range(
                        len(categories)
                    ):

                        for j in range(
                            i + 1,
                            len(categories)
                        ):

                            pairs.append(
                                (
                                    categories[i],
                                    categories[j]
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

            return (
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
                title="Top Category Combinations Bought Together",
                labels={
                    "frequency":
                        "Co-purchase Frequency",
                    "pair":
                        "Category Pair"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=500,
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Items per order
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            items_per_order = (
                order_items
                .groupby("order_id")
                ["order_item_id"]
                .count()
                .reset_index()
            )

            items_per_order.columns = [
                "order_id",
                "items_count"
            ]

            items_distribution = (
                items_per_order[
                    "items_count"
                ]
                .value_counts()
                .head(10)
                .reset_index()
            )

            items_distribution.columns = [
                "items_in_order",
                "order_count"
            ]

            fig = px.bar(
                items_distribution,
                x="items_in_order",
                y="order_count",
                title="Items per Order Distribution",
                labels={
                    "items_in_order":
                        "Items in Order",
                    "order_count":
                        "Number of Orders"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            category_orders = (
                order_products
                .groupby(
                    "product_category_name"
                )["order_id"]
                .nunique()
                .reset_index()
                .sort_values(
                    "order_id",
                    ascending=False
                )
                .head(10)
            )

            category_orders.columns = [
                "category",
                "order_count"
            ]

            fig = px.bar(
                category_orders,
                x="order_count",
                y="category",
                orientation="h",
                title="Categories with Highest Order Presence",
                labels={
                    "order_count":
                        "Orders",
                    "category":
                        "Product Category"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                height=400,
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Recommendation demo
        # ----------------------------------------------------

        st.subheader("💡 Recommendation Explorer")

        if not pair_counts.empty:

            category_options = sorted(
                set(
                    pair_counts["category_1"]
                ).union(
                    set(
                        pair_counts["category_2"]
                    )
                )
            )

            selected_category = st.selectbox(
                "Select a category",
                category_options
            )

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

                    recommendation = (
                        row["category_2"]
                        if row["category_1"]
                        == selected_category
                        else row["category_1"]
                    )

                    st.markdown(
                        f"""
                        <div class="insight-card">

                            <div class="insight-title">
                                🛒 {recommendation}
                            </div>

                            <div class="insight-text">
                                Frequently co-purchased with
                                <strong>
                                    {selected_category}
                                </strong>
                                in
                                <strong>
                                    {int(row["frequency"]):,}
                                </strong>
                                orders.
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.info(
            "💡 These associations can support bundle creation, "
            "cross-selling and recommendation strategies. "
            "They represent observed co-purchase frequency, "
            "not a machine-learning recommendation model."
        )

    # ========================================================
    # TAB 5 — SQL SHOWCASE
    # ========================================================

    with tab5:

        st.markdown(
            '<div class="section-title">📝 SQL Analysis Showcase</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="insight-card">

                <div class="insight-title">
                    🔎 From SQL to Business Insights
                </div>

                <div class="insight-text">
                    The queries below demonstrate how the key
                    business metrics were calculated from the
                    Olist relational dataset.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # Revenue
        # ----------------------------------------------------

        st.subheader("💰 Revenue & Payment Analysis")

        with st.expander(
            "KPI 1 — Total Payment Value",
            expanded=True
        ):

            st.code(
                """
SELECT
    ROUND(SUM(payment_value), 2)
        AS total_payment_value
FROM payments;
                """,
                language="sql"
            )

            st.caption(
                "Measures total recorded payment value. "
                "This is a payment-based metric, not "
                "formal accounting revenue recognition."
            )

        with st.expander(
            "KPI 2 — Monthly Payment Value"
        ):

            st.code(
                """
SELECT
    DATE_FORMAT(
        o.order_purchase_timestamp,
        '%Y-%m'
    ) AS purchase_month,
    ROUND(
        SUM(p.payment_value),
        2
    ) AS total_payment_value
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY purchase_month
ORDER BY purchase_month;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 3 — Top Product Categories"
        ):

            st.code(
                """
SELECT
    pr.product_category_name,
    ROUND(
        SUM(oi.price),
        2
    ) AS product_item_value
FROM products pr
JOIN order_items oi
    ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name
ORDER BY product_item_value DESC
LIMIT 10;
                """,
                language="sql"
            )

            st.caption(
                "Category performance is calculated using "
                "product-item prices."
            )

        with st.expander(
            "KPI 4 — State-Wise Payment Value"
        ):

            st.code(
                """
SELECT
    c.customer_state,
    ROUND(
        SUM(p.payment_value),
        2
    ) AS state_payment_value
FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id
JOIN payments p
    ON p.order_id = o.order_id
GROUP BY c.customer_state
ORDER BY state_payment_value DESC;
                """,
                language="sql"
            )

        # ----------------------------------------------------
        # Orders
        # ----------------------------------------------------

        st.subheader("📦 Order Analysis")

        with st.expander(
            "KPI 5 — Total Orders"
        ):

            st.code(
                """
SELECT
    COUNT(DISTINCT order_id)
        AS total_orders
FROM orders;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 6 — Monthly Order Trend"
        ):

            st.code(
                """
SELECT
    DATE_FORMAT(
        order_purchase_timestamp,
        '%Y-%m'
    ) AS purchase_month,
    COUNT(DISTINCT order_id)
        AS total_orders
FROM orders
GROUP BY purchase_month
ORDER BY purchase_month;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 7 — Order Status Distribution"
        ):

            st.code(
                """
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 8 — Average Order Payment"
        ):

            st.code(
                """
SELECT
    ROUND(
        AVG(order_payment),
        2
    ) AS average_order_payment
FROM (
    SELECT
        order_id,
        SUM(payment_value)
            AS order_payment
    FROM payments
    GROUP BY order_id
) t;
                """,
                language="sql"
            )

        # ----------------------------------------------------
        # Customers
        # ----------------------------------------------------

        st.subheader("👥 Customer Analysis")

        with st.expander(
            "KPI 9 — Unique Customers"
        ):

            st.code(
                """
SELECT
    COUNT(
        DISTINCT c.customer_unique_id
    ) AS unique_customers
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 10 — Repeat Customer Rate"
        ):

            st.code(
                """
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
        COUNT(
            DISTINCT o.order_id
        ) AS purchase_count

    FROM orders o

    JOIN customers c
        ON o.customer_id =
           c.customer_id

    GROUP BY
        c.customer_unique_id
) t;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 11 — Customer Segmentation"
        ):

            st.code(
                """
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

        COUNT(
            DISTINCT o.order_id
        ) AS total_orders

    FROM orders o

    JOIN customers c
        ON o.customer_id =
           c.customer_id

    GROUP BY
        c.customer_unique_id

) t

GROUP BY customer_segment
ORDER BY total_customers DESC;
                """,
                language="sql"
            )

        with st.expander(
            "KPI 12 — Top Customers by Lifetime Payment Value"
        ):

            st.code(
                """
SELECT
    c.customer_unique_id,

    ROUND(
        SUM(p.payment_value),
        2
    ) AS customer_lifetime_payment

FROM orders o

JOIN customers c
    ON o.customer_id =
       c.customer_id

JOIN payments p
    ON p.order_id =
       o.order_id

GROUP BY
    c.customer_unique_id

ORDER BY
    customer_lifetime_payment DESC

LIMIT 10;
                """,
                language="sql"
            )

        # ----------------------------------------------------
        # Dataset Metrics
        # ----------------------------------------------------

        st.subheader("🗂️ Dataset Validation")

        validation_data = pd.DataFrame({
            "Metric": [
                "Orders",
                "Unique Products",
                "Product Categories",
                "Unique Customers"
            ],
            "Value": [
                f"{orders['order_id'].nunique():,}",
                f"{products['product_id'].nunique():,}",
                f"{products['product_category_name'].nunique():,}",
                f"{customers['customer_unique_id'].nunique():,}"
            ]
        })

        st.dataframe(
            validation_data,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # Analysis Approach — ONLY HERE
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="approach-card">

                <h3 style="
                    color: #a5b4fc;
                    margin-bottom: 1rem;
                ">
                    🧭 Analysis Approach
                </h3>

                <div class="approach-step">
                    <span class="step-number">01</span>
                    Validated the raw Olist datasets and
                    checked data quality, relationships,
                    NULL values and business rules.
                </div>

                <div class="approach-step">
                    <span class="step-number">02</span>
                    Created cleaned analysis tables while
                    preserving the original raw datasets.
                </div>

                <div class="approach-step">
                    <span class="step-number">03</span>
                    Used SQL to calculate revenue,
                    order, customer, product and
                    geographic KPIs.
                </div>

                <div class="approach-step">
                    <span class="step-number">04</span>
                    Used Python, Pandas and Plotly to
                    validate and visualize the findings.
                </div>

                <div class="approach-step">
                    <span class="step-number">05</span>
                    Built and deployed an interactive
                    Streamlit business intelligence dashboard.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # FOOTER — ONLY ONCE
    # ========================================================

    st.markdown(
        """
        <div class="footer">

            <div style="
                font-size: 1rem;
                margin-bottom: 0.5rem;
            ">
                <strong>
                    📊 Olist E-Commerce Intelligence
                </strong>
            </div>

            <div>
                Built by <strong>Varshini A S</strong>
                &nbsp;•&nbsp;
                Data Science & AI
                &nbsp;•&nbsp;
                SQL & Python
            </div>

            <div style="
                margin-top: 0.5rem;
                font-size: 0.85rem;
            ">
                Open to Data Analyst,
                Business Analyst & Data Science
                internship opportunities.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Upload the required Olist CSV files to "
        "`01_dataset/00_raw_data/` to launch the dashboard."
    )
