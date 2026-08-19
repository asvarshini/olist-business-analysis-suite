import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Olist Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("📊 Olist E-Commerce Analytics")
st.markdown("Brazilian E-Commerce Business Intelligence | 100K+ Orders Analyzed")

# ============================================================
# LOAD DATA - SMART PATH
# Works both locally and on Streamlit Cloud
# ============================================================

@st.cache_data
def load_data():

    def get_data_path(filename):
        local_path = f'../../01_dataset/00_raw_data/{filename}'
        cloud_path = f'01_dataset/00_raw_data/{filename}'

        return local_path if os.path.exists(local_path) else cloud_path

    orders = pd.read_csv(
        get_data_path('olist_orders_dataset.csv')
    )

    order_items = pd.read_csv(
        get_data_path('olist_order_items_dataset.csv')
    )

    payments = pd.read_csv(
        get_data_path('olist_order_payments_dataset.csv')
    )

    customers = pd.read_csv(
        get_data_path('olist_customers_dataset.csv')
    )

    products = pd.read_csv(
        get_data_path('olist_products_dataset.csv')
    )

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    orders['order_purchase_timestamp'] = pd.to_datetime(
        orders['order_purchase_timestamp']
    )

    orders['order_month'] = (
        orders['order_purchase_timestamp']
        .dt.to_period('M')
        .astype(str)
    )

    return (
        orders,
        order_items,
        payments,
        customers,
        products
    )


# ============================================================
# TRY TO LOAD DATA
# ============================================================

try:

    orders, order_items, payments, customers, products = load_data()

    data_loaded = True

except Exception as e:

    st.error(f"Error loading data: {e}")

    st.info(
        "Make sure CSV files are in "
        "01_dataset/00_raw_data/"
    )

    data_loaded = False


# ============================================================
# MAIN APPLICATION
# ============================================================

if data_loaded:

    # ========================================================
    # SIDEBAR FILTERS
    # ========================================================

    st.sidebar.header("🔍 Filters")

    # --------------------------------------------------------
    # Date range
    # --------------------------------------------------------

    min_date = (
        orders['order_purchase_timestamp']
        .min()
        .date()
    )

    max_date = (
        orders['order_purchase_timestamp']
        .max()
        .date()
    )

    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # --------------------------------------------------------
    # State filter
    # --------------------------------------------------------

    states = (
        ['All']
        + sorted(
            customers['customer_state']
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_state = st.sidebar.selectbox(
        "State",
        states
    )

    # ========================================================
    # FILTER DATA
    # ========================================================

    # IMPORTANT:
    # Include the ENTIRE final selected date.
    #
    # Previously <= pd.Timestamp(date_range[1])
    # stopped at midnight of the final date.
    #
    # Using < final_date + 1 day includes the complete day.

    if len(date_range) == 2:

        start_date = pd.Timestamp(date_range[0])

        end_date = (
            pd.Timestamp(date_range[1])
            + pd.Timedelta(days=1)
        )

        mask = (
            (orders['order_purchase_timestamp'] >= start_date)
            &
            (orders['order_purchase_timestamp'] < end_date)
        )

    else:

        # Safety fallback if only one date is selected
        selected_date = pd.Timestamp(date_range[0])

        mask = (
            (orders['order_purchase_timestamp'] >= selected_date)
            &
            (
                orders['order_purchase_timestamp']
                < selected_date + pd.Timedelta(days=1)
            )
        )

    filtered_orders = orders[mask].copy()

    # --------------------------------------------------------
    # State filter
    # --------------------------------------------------------

    if selected_state != 'All':

        state_customers = customers[
            customers['customer_state'] == selected_state
        ]['customer_id']

        filtered_orders = filtered_orders[
            filtered_orders['customer_id'].isin(
                state_customers
            )
        ]

    # ========================================================
    # MERGES FOR CALCULATIONS
    # ========================================================

    orders_with_payments = filtered_orders.merge(
        payments,
        on='order_id',
        how='left'
    )

    orders_with_items = filtered_orders.merge(
        order_items,
        on='order_id',
        how='left'
    )

    orders_full = filtered_orders.merge(
        customers,
        on='customer_id',
        how='left'
    )

    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    with col1:

        total_revenue = (
            orders_with_payments['payment_value']
            .sum()
        )

        st.metric(
            "💰 Revenue",
            f"R$ {total_revenue:,.0f}"
        )

    # --------------------------------------------------------
    # Orders
    # --------------------------------------------------------

    with col2:

        total_orders = (
            filtered_orders['order_id']
            .nunique()
        )

        st.metric(
            "📦 Orders",
            f"{total_orders:,}"
        )

    # --------------------------------------------------------
    # AOV
    # --------------------------------------------------------

    with col3:

        order_payment_totals = (
            orders_with_payments
            .groupby('order_id')['payment_value']
            .sum()
        )

        aov = order_payment_totals.mean()

        st.metric(
            "📈 AOV",
            f"R$ {aov:,.0f}"
        )

    # --------------------------------------------------------
    # Customers
    # --------------------------------------------------------

    with col4:

        filtered_customer_ids = (
            filtered_orders['customer_id']
            .dropna()
        )

        total_customers = (
            customers[
                customers['customer_id'].isin(
                    filtered_customer_ids
                )
            ]['customer_unique_id']
            .nunique()
        )

        st.metric(
            "👥 Customers",
            f"{total_customers:,}"
        )

    # --------------------------------------------------------
    # Products
    # --------------------------------------------------------

    with col5:

        total_products = (
            orders_with_items['product_id']
            .nunique()
        )

        st.metric(
            "🏷️ Products",
            f"{total_products:,}"
        )

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
    # TAB 1: REVENUE
    # ========================================================

    with tab1:

        st.header("Revenue Performance")

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Monthly Revenue
        # ----------------------------------------------------

        with col1:

            monthly_rev = (
                orders_with_payments
                .groupby('order_month')['payment_value']
                .sum()
                .reset_index()
            )

            fig = px.line(
                monthly_rev,
                x='order_month',
                y='payment_value',
                title='Monthly Revenue Trend',
                markers=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Category Revenue
        # ----------------------------------------------------

        with col2:

            items_prod = orders_with_items.merge(
                products,
                on='product_id',
                how='left'
            )

            cat_rev = (
                items_prod
                .groupby('product_category_name')['price']
                .sum()
                .reset_index()
            )

            cat_rev = (
                cat_rev
                .sort_values(
                    'price',
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                cat_rev,
                x='price',
                y='product_category_name',
                orientation='h',
                title='Top 10 Categories by Revenue'
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ========================================================
    # TAB 2: ORDERS
    # ========================================================

    with tab2:

        st.header("Order Performance")

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Monthly Orders
        # ----------------------------------------------------

        with col1:

            monthly_orders = (
                filtered_orders
                .groupby('order_month')['order_id']
                .nunique()
                .reset_index()
            )

            fig = px.bar(
                monthly_orders,
                x='order_month',
                y='order_id',
                title='Monthly Order Volume'
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Order Status
        # ----------------------------------------------------

        with col2:

            status_counts = (
                filtered_orders['order_status']
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                'status',
                'count'
            ]

            fig = px.pie(
                status_counts,
                values='count',
                names='status',
                title='Order Status Distribution',
                hole=0.4
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ========================================================
    # TAB 3: CUSTOMERS
    # ========================================================

    with tab3:

        st.header("Customer Insights")

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Customer Segmentation
        # ----------------------------------------------------

        with col1:

            orders_with_unique = filtered_orders.merge(
                customers[
                    [
                        'customer_id',
                        'customer_unique_id'
                    ]
                ],
                on='customer_id',
                how='left'
            )

            cust_orders = (
                orders_with_unique
                .groupby(
                    'customer_unique_id'
                )['order_id']
                .nunique()
                .reset_index()
            )

            cust_orders.columns = [
                'customer_unique_id',
                'order_count'
            ]

            def segment(count):

                if count == 1:
                    return 'Low Frequency'

                elif count <= 5:
                    return 'Medium Frequency'

                else:
                    return 'High Frequency'

            cust_orders['segment'] = (
                cust_orders['order_count']
                .apply(segment)
            )

            seg_counts = (
                cust_orders['segment']
                .value_counts()
                .reset_index()
            )

            seg_counts.columns = [
                'segment',
                'count'
            ]

            fig = px.pie(
                seg_counts,
                values='count',
                names='segment',
                title='Customer Segmentation',
                color='segment',
                color_discrete_map={
                    'Low Frequency': '#ff6b6b',
                    'Medium Frequency': '#feca57',
                    'High Frequency': '#48dbfb'
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Customers by State
        # ----------------------------------------------------

        with col2:

            state_cust = (
                customers
                .groupby(
                    'customer_state'
                )['customer_unique_id']
                .nunique()
                .reset_index()
            )

            state_cust = (
                state_cust
                .sort_values(
                    'customer_unique_id',
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                state_cust,
                x='customer_state',
                y='customer_unique_id',
                title='Top 10 States by Customers'
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ========================================================
    # TAB 4: RECOMMENDATIONS
    # ========================================================

    with tab4:

        st.header("🤖 AI Product Recommendations")

        st.markdown(
            "**Co-purchase analysis** — discover what products "
            "are frequently bought together"
        )

        items_with_products = order_items.merge(
            products[
                [
                    'product_id',
                    'product_category_name'
                ]
            ],
            on='product_id',
            how='left'
        )

        category_mapping = (
            products[
                [
                    'product_id',
                    'product_category_name'
                ]
            ]
            .drop_duplicates()
        )

        # ----------------------------------------------------
        # Section 1: Product Associations
        # ----------------------------------------------------

        st.subheader(
            "🔗 Frequently Bought Together"
        )

        order_products = (
            order_items.merge(
                products[
                    [
                        'product_id',
                        'product_category_name'
                    ]
                ],
                on='product_id',
                how='left'
            )
            [
                [
                    'order_id',
                    'product_id',
                    'product_category_name'
                ]
            ]
        )

        @st.cache_data
        def get_product_pairs(order_products):

            pairs = []

            for order_id, group in order_products.groupby(
                'order_id'
            ):

                products_in_order = (
                    group[
                        'product_category_name'
                    ]
                    .dropna()
                    .unique()
                )

                if len(products_in_order) > 1:

                    for i, cat1 in enumerate(
                        products_in_order
                    ):

                        for cat2 in products_in_order[
                            i + 1:
                        ]:

                            if cat1 != cat2:

                                pairs.append(
                                    (cat1, cat2)
                                )

            pairs_df = pd.DataFrame(
                pairs,
                columns=[
                    'category_1',
                    'category_2'
                ]
            )

            if pairs_df.empty:
                return pd.DataFrame(
                    columns=[
                        'category_1',
                        'category_2',
                        'frequency'
                    ]
                )

            pair_counts = (
                pairs_df
                .groupby(
                    [
                        'category_1',
                        'category_2'
                    ]
                )
                .size()
                .reset_index(
                    name='frequency'
                )
            )

            pair_counts = (
                pair_counts
                .sort_values(
                    'frequency',
                    ascending=False
                )
                .head(15)
            )

            return pair_counts

        pair_counts = get_product_pairs(
            order_products
        )

        if not pair_counts.empty:

            top_pairs = pair_counts.head(10).copy()

            top_pairs['category_pair'] = (
                top_pairs['category_1']
                + " + "
                + top_pairs['category_2']
            )

            fig = px.bar(
                top_pairs,
                x='frequency',
                y='category_pair',
                orientation='h',
                title='Top 10 Category Combinations (Bought Together)',
                labels={
                    'frequency':
                        'Times Bought Together',
                    'category_pair':
                        'Category Pair'
                },
                color='frequency',
                color_continuous_scale='Viridis'
            )

            fig.update_layout(
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough multi-item orders in selected "
                "date range for association analysis."
            )

        # ----------------------------------------------------
        # Section 2: Cross-Category Insights
        # ----------------------------------------------------

        st.subheader(
            "🎯 Cross-Category Buying Patterns"
        )

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # Items per Order
        # ----------------------------------------------------

        with col1:

            items_per_order = (
                order_items
                .groupby('order_id')['order_item_id']
                .count()
                .reset_index()
            )

            items_per_order.columns = [
                'order_id',
                'items_count'
            ]

            items_dist = (
                items_per_order[
                    'items_count'
                ]
                .value_counts()
                .head(10)
                .reset_index()
            )

            items_dist.columns = [
                'items_in_order',
                'order_count'
            ]

            fig = px.bar(
                items_dist,
                x='items_in_order',
                y='order_count',
                title='Items per Order Distribution',
                labels={
                    'items_in_order':
                        'Items in Order',
                    'order_count':
                        'Number of Orders'
                },
                color='order_count',
                color_continuous_scale='Plasma'
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Category Order Presence
        # ----------------------------------------------------

        with col2:

            cross_sell = order_items.merge(
                products[
                    [
                        'product_id',
                        'product_category_name'
                    ]
                ],
                on='product_id',
                how='left'
            )

            category_orders = (
                cross_sell
                .groupby(
                    'product_category_name'
                )['order_id']
                .nunique()
                .reset_index()
            )

            category_orders.columns = [
                'category',
                'order_count'
            ]

            category_orders = (
                category_orders
                .sort_values(
                    'order_count',
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                category_orders,
                x='order_count',
                y='category',
                orientation='h',
                title='Categories with Highest Order Presence',
                labels={
                    'order_count':
                        'Orders Containing Category',
                    'category':
                        'Product Category'
                },
                color='order_count',
                color_continuous_scale='Cividis'
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # Recommendation Engine
        # ----------------------------------------------------

        st.subheader(
            "💡 Smart Recommendations"
        )

        top_categories = (
            products[
                'product_category_name'
            ]
            .dropna()
            .value_counts()
            .head(20)
            .index
            .tolist()
        )

        selected_category = st.selectbox(
            "Select a product category to see recommendations:",
            options=top_categories,
            index=0
        )

        if selected_category:

            related_pairs = pair_counts[
                (
                    pair_counts['category_1']
                    == selected_category
                )
                |
                (
                    pair_counts['category_2']
                    == selected_category
                )
            ].head(5)

            if not related_pairs.empty:

                st.markdown(
                    f"**Customers who bought "
                    f"`{selected_category}` also bought:**"
                )

                max_frequency = (
                    pair_counts['frequency'].max()
                )

                for _, row in related_pairs.iterrows():

                    rec_category = (
                        row['category_2']
                        if row['category_1']
                        == selected_category
                        else row['category_1']
                    )

                    confidence = min(
                        100,
                        int(
                            (
                                row['frequency']
                                / max_frequency
                            ) * 100
                        )
                    )

                    st.markdown(
                        f"""
                        <div style="
                            background: linear-gradient(
                                135deg,
                                rgba(99,102,241,0.1),
                                rgba(6,182,212,0.1)
                            );
                            border-left: 4px solid #6366f1;
                            padding: 1rem 1.5rem;
                            border-radius: 0 12px 12px 0;
                            margin-bottom: 0.8rem;
                        ">
                            <strong style="
                                color: #6366f1;
                                font-size: 1.1rem;
                            ">
                                {rec_category}
                            </strong>

                            <div style="
                                color: #94a3b8;
                                font-size: 0.9rem;
                                margin-top: 0.3rem;
                            ">
                                Confidence: {confidence}%
                                |
                                Co-purchased
                                {row['frequency']} times
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.info(
                    f"Not enough data for "
                    f"`{selected_category}` "
                    f"in current filter range."
                )

        st.markdown(
            """
            <div style="
                background: rgba(245,158,11,0.1);
                border: 1px solid rgba(245,158,11,0.3);
                border-radius: 16px;
                padding: 1.5rem;
                margin-top: 1rem;
            ">
                <h4 style="
                    color: #f59e0b;
                    margin-bottom: 0.5rem;
                ">
                    📊 Business Insight
                </h4>

                <p style="
                    color: #cbd5e1;
                    margin: 0;
                ">
                    Cross-category recommendations can support
                    higher average order value through bundle
                    pricing, email marketing, and homepage
                    personalization.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # TAB 5: SQL SHOWCASE
    # ========================================================

    with tab5:

        st.header(
            "📝 SQL Analysis Behind the Dashboard"
        )

        st.markdown(
            "**These are the actual SQL queries** written "
            "to analyze the Olist dataset. The dashboard "
            "visualizes the output of these queries."
        )

        # ----------------------------------------------------
        # REVENUE SQL
        # ----------------------------------------------------

        st.subheader("💰 Revenue Analysis")

        with st.expander(
            "📌 KPI 1: Total Company Revenue",
            expanded=True
        ):

            st.code(
                """
-- Total revenue from all orders
SELECT
    ROUND(SUM(payment_value), 2) AS total_revenue
FROM payments;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Result: "
                "R$ 16,008,872.12</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 2: Monthly Revenue Trend"
        ):

            st.code(
                """
-- Revenue trend over time
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
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Shows seasonal patterns "
                "and monthly revenue trends.</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 3: Top Product Categories by Revenue"
        ):

            st.code(
                """
-- Revenue by product category
SELECT
    pr.product_category_name,
    ROUND(
        SUM(oi.price),
        2
    ) AS product_category_revenue
FROM products pr
JOIN order_items oi
    ON oi.product_id = pr.product_id
GROUP BY pr.product_category_name
ORDER BY product_category_revenue DESC
LIMIT 10;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Top category: "
                "Beauty & Health — "
                "R$ 1,258,681.34</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 4: State-Wise Revenue"
        ):

            st.code(
                """
-- Revenue by Brazilian state
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
ORDER BY state_revenue DESC
LIMIT 10;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>São Paulo (SP) leads "
                "with approximately 37.47% of "
                "total payment revenue.</i></small>",
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # ORDERS SQL
        # ----------------------------------------------------

        st.subheader("📦 Order Performance")

        with st.expander(
            "📌 KPI 5: Total Orders"
        ):

            st.code(
                """
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Result: "
                "99,441 orders</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 6: Monthly Order Trend"
        ):

            st.code(
                """
SELECT
    DATE_FORMAT(
        order_purchase_timestamp,
        '%Y-%m'
    ) AS monthly_purchase,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY monthly_purchase
ORDER BY monthly_purchase;
                """,
                language='sql'
            )

        with st.expander(
            "📌 KPI 7: Order Status Distribution"
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
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>97.02% of orders "
                "were delivered.</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 8: Average Order Value (AOV)"
        ):

            st.code(
                """
SELECT
    AVG(t.order_total) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(price) AS order_total
    FROM order_items
    GROUP BY order_id
) t;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Payment-based AOV: "
                "R$ 160.99</i></small>",
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # CUSTOMER SQL
        # ----------------------------------------------------

        st.subheader("👥 Customer Insights")

        with st.expander(
            "📌 KPI 9: Repeat Customer Rate"
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
        COUNT(DISTINCT o.order_id)
            AS purchase_count
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
) t;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Repeat customer rate: "
                "3.12%</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 10: Customer Segmentation"
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
        COUNT(DISTINCT o.order_id)
            AS total_orders
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
) t
GROUP BY customer_segment
ORDER BY total_customers DESC;
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>96.88% Low Frequency, "
                "3.11% Medium Frequency, "
                "0.01% High Frequency.</i></small>",
                unsafe_allow_html=True
            )

        with st.expander(
            "📌 KPI 11: Top Customers by Lifetime Revenue"
        ):

            st.code(
                """
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
                """,
                language='sql'
            )

            st.markdown(
                "<small>💡 <i>Top customer lifetime "
                "revenue: R$ 13,664.08</i></small>",
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # SQL SKILLS
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader(
            "🛠️ SQL Skills Demonstrated"
        )

        skills_data = {

            "Skill": [
                "Complex Joins",
                "Aggregation",
                "Subqueries",
                "Date Functions",
                "Case Statements",
                "Window Functions"
            ],

            "Example": [
                "4-table joins (orders, customers, payments, items)",
                "SUM(), COUNT(), AVG() with GROUP BY",
                "Customer lifetime revenue calculation",
                "DATE_FORMAT() for time-series analysis",
                "Customer segmentation logic",
                "Ranking and row numbering"
            ]
        }

        st.table(
            pd.DataFrame(skills_data)
        )

        st.markdown(
            """
            <div style="
                background: linear-gradient(
                    135deg,
                    rgba(99,102,241,0.1),
                    rgba(6,182,212,0.1)
                );
                border-radius: 16px;
                padding: 1.5rem;
                margin-top: 1rem;
            ">

                <h4 style="
                    color: #6366f1;
                    margin-bottom: 0.5rem;
                ">
                    📊 Analysis Approach
                </h4>

                <p style="
                    color: #cbd5e1;
                    margin: 0;
                ">

                    <strong>Step 1:</strong>
                    Validated and cleaned the Olist datasets
                    <br>

                    <strong>Step 2:</strong>
                    Wrote SQL queries to extract business KPIs
                    <br>

                    <strong>Step 3:</strong>
                    Validated insights using Python
                    <br>

                    <strong>Step 4:</strong>
                    Built an interactive Streamlit dashboard
                    <br>

                    <strong>Step 5:</strong>
                    Deployed the dashboard for business analysis

                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("---")

    st.markdown(
        """
        <div style='text-align: center; color: #666;'>

            <p>
                Built by <b>Varshini A S</b>
                |
                IIT Roorkee Data Science
                |
                GSSoC 2026
            </p>

            <p>
                📧 asvarshini84@gmail.com
                |
                💼 Open for internships & freelance work
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Upload data files to "
        "01_dataset/00_raw_data/ "
        "to get started"
    )
