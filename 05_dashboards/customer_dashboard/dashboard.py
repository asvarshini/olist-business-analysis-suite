import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page config
st.set_page_config(
    page_title="Olist Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Olist E-Commerce Analytics")
st.markdown("Brazilian E-Commerce Business Intelligence | 100K+ Orders Analyzed")

# Load data - SMART PATH (works both local and cloud)
@st.cache_data
def load_data():
    def get_data_path(filename):
        local_path = f'../../01_dataset/00_raw_data/{filename}'
        cloud_path = f'01_dataset/00_raw_data/{filename}'
        return local_path if os.path.exists(local_path) else cloud_path
    
    orders = pd.read_csv(get_data_path('olist_orders_dataset.csv'))
    order_items = pd.read_csv(get_data_path('olist_order_items_dataset.csv'))
    payments = pd.read_csv(get_data_path('olist_order_payments_dataset.csv'))
    customers = pd.read_csv(get_data_path('olist_customers_dataset.csv'))
    products = pd.read_csv(get_data_path('olist_products_dataset.csv'))
    
    # Convert dates
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    return orders, order_items, payments, customers, products

# Try to load
try:
    orders, order_items, payments, customers, products = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure CSV files are in 01_dataset/00_raw_data/")
    data_loaded = False

if data_loaded:
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range
    min_date = orders['order_purchase_timestamp'].min().date()
    max_date = orders['order_purchase_timestamp'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # State filter
    states = ['All'] + sorted(customers['customer_state'].unique().tolist())
    selected_state = st.sidebar.selectbox("State", states)
    
    # Filter data
    mask = (orders['order_purchase_timestamp'] >= pd.Timestamp(date_range[0])) & \
           (orders['order_purchase_timestamp'] <= pd.Timestamp(date_range[1]))
    filtered_orders = orders[mask]
    
    if selected_state != 'All':
        state_customers = customers[customers['customer_state'] == selected_state]['customer_id']
        filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(state_customers)]
    
    # Merge for calculations
    orders_with_payments = filtered_orders.merge(payments, on='order_id', how='left')
    orders_with_items = filtered_orders.merge(order_items, on='order_id', how='left')
    orders_full = filtered_orders.merge(customers, on='customer_id', how='left')
    
    # ==================== KPI CARDS ====================
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_revenue = orders_with_payments['payment_value'].sum()
        st.metric("💰 Revenue", f"R$ {total_revenue:,.0f}")
    
    with col2:
        total_orders = filtered_orders['order_id'].nunique()
        st.metric("📦 Orders", f"{total_orders:,}")
    
    with col3:
        aov = orders_with_payments.groupby('order_id')['payment_value'].sum().mean()
        st.metric("📈 AOV", f"R$ {aov:,.0f}")
    
    with col4:
        total_customers = filtered_orders['customer_id'].nunique()
        st.metric("👥 Customers", f"{total_customers:,}")
    
    with col5:
        total_products = orders_with_items['product_id'].nunique()
        st.metric("🏷️ Products", f"{total_products:,}")
    
    # ==================== TABS ====================
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Revenue", "📦 Orders", "👥 Customers", "🤖 Recommendations"])
    
    # ==================== TAB 1: REVENUE ====================
    with tab1:
        st.header("Revenue Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_rev = orders_with_payments.groupby('order_month')['payment_value'].sum().reset_index()
            fig = px.line(monthly_rev, x='order_month', y='payment_value', 
                         title='Monthly Revenue Trend', markers=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            items_prod = orders_with_items.merge(products, on='product_id', how='left')
            cat_rev = items_prod.groupby('product_category_name')['price'].sum().reset_index()
            cat_rev = cat_rev.sort_values('price', ascending=False).head(10)
            fig = px.bar(cat_rev, x='price', y='product_category_name', 
                        orientation='h', title='Top 10 Categories by Revenue')
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 2: ORDERS ====================
    with tab2:
        st.header("Order Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_orders = filtered_orders.groupby('order_month')['order_id'].nunique().reset_index()
            fig = px.bar(monthly_orders, x='order_month', y='order_id',
                        title='Monthly Order Volume')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            status_counts = filtered_orders['order_status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            fig = px.pie(status_counts, values='count', names='status',
                        title='Order Status Distribution', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 3: CUSTOMERS ====================
    with tab3:
        st.header("Customer Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            orders_with_unique = filtered_orders.merge(
                customers[['customer_id', 'customer_unique_id']], 
                on='customer_id', 
                how='left'
            )
            cust_orders = orders_with_unique.groupby('customer_unique_id')['order_id'].nunique().reset_index()
            cust_orders.columns = ['customer_unique_id', 'order_count']
            
            def segment(count):
                if count == 1: return 'Low Frequency'
                elif count <= 5: return 'Medium Frequency'
                else: return 'High Frequency'
            
            cust_orders['segment'] = cust_orders['order_count'].apply(segment)
            seg_counts = cust_orders['segment'].value_counts().reset_index()
            seg_counts.columns = ['segment', 'count']
            
            fig = px.pie(seg_counts, values='count', names='segment',
                        title='Customer Segmentation',
                        color='segment',
                        color_discrete_map={
                            'Low Frequency': '#ff6b6b',
                            'Medium Frequency': '#feca57',
                            'High Frequency': '#48dbfb'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            state_cust = customers.groupby('customer_state')['customer_unique_id'].nunique().reset_index()
            state_cust = state_cust.sort_values('customer_unique_id', ascending=False).head(10)
            fig = px.bar(state_cust, x='customer_state', y='customer_unique_id',
                        title='Top 10 States by Customers')
            st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 4: RECOMMENDATIONS (NEW!) ====================
    with tab4:
        st.header("🤖 AI Product Recommendations")
        st.markdown("**Co-purchase analysis** — discover what products are frequently bought together")
        
        # Prepare data for recommendation analysis
        # Get all order-items with product info
        items_with_products = order_items.merge(products[['product_id', 'product_category_name']], 
                                                 on='product_id', how='left')
        
        # Get category names for better display
        category_mapping = products[['product_id', 'product_category_name']].drop_duplicates()
        
        # --- Section 1: Top Product Associations ---
        st.subheader("🔗 Frequently Bought Together")
        
        # Find products bought in same order
        order_products = order_items.merge(
            products[['product_id', 'product_category_name']], 
            on='product_id', 
            how='left'
        )[['order_id', 'product_id', 'product_category_name']]
        
        # Get top product pairs
        @st.cache_data
        def get_product_pairs():
            # Create pairs of products in same order
            pairs = []
            for order_id, group in order_products.groupby('order_id'):
                products_in_order = group['product_category_name'].unique()
                if len(products_in_order) > 1:
                    for i, cat1 in enumerate(products_in_order):
                        for cat2 in products_in_order[i+1:]:
                            if cat1 != cat2:
                                pairs.append((cat1, cat2))
            
            pairs_df = pd.DataFrame(pairs, columns=['category_1', 'category_2'])
            pair_counts = pairs_df.groupby(['category_1', 'category_2']).size().reset_index(name='frequency')
            pair_counts = pair_counts.sort_values('frequency', ascending=False).head(15)
            return pair_counts
        
        pair_counts = get_product_pairs()
        
        if not pair_counts.empty:
            # Create network-style visualization
            fig = px.bar(
                pair_counts.head(10),
                x='frequency',
                y=pair_counts.head(10).apply(lambda x: f"{x['category_1']} + {x['category_2']}", axis=1),
                orientation='h',
                title='Top 10 Category Combinations (Bought Together)',
                labels={'frequency': 'Times Bought Together', 'y': 'Category Pair'},
                color='frequency',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough multi-item orders in selected date range for association analysis.")
        
        # --- Section 2: Cross-Category Insights ---
        st.subheader("🎯 Cross-Category Buying Patterns")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Products per order distribution
            items_per_order = order_items.groupby('order_id')['order_item_id'].count().reset_index()
            items_per_order.columns = ['order_id', 'items_count']
            
            items_dist = items_per_order['items_count'].value_counts().head(10).reset_index()
            items_dist.columns = ['items_in_order', 'order_count']
            
            fig = px.bar(
                items_dist,
                x='items_in_order',
                y='order_count',
                title='Items per Order Distribution',
                labels={'items_in_order': 'Items in Order', 'order_count': 'Number of Orders'},
                color='order_count',
                color_continuous_scale='Plasma'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top categories by cross-sell potential
            cross_sell = order_items.merge(
                products[['product_id', 'product_category_name']], 
                on='product_id', 
                how='left'
            )
            
            # Count how many orders each category appears in
            category_orders = cross_sell.groupby('product_category_name')['order_id'].nunique().reset_index()
            category_orders.columns = ['category', 'order_count']
            category_orders = category_orders.sort_values('order_count', ascending=False).head(10)
            
            fig = px.bar(
                category_orders,
                x='order_count',
                y='category',
                orientation='h',
                title='Categories with Highest Order Presence',
                labels={'order_count': 'Orders Containing Category', 'category': 'Product Category'},
                color='order_count',
                color_continuous_scale='Cividis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # --- Section 3: Recommendation Engine Demo ---
        st.subheader("💡 Smart Recommendations")
        
        # Get top categories for dropdown
        top_categories = products['product_category_name'].value_counts().head(20).index.tolist()
        
        selected_category = st.selectbox(
            "Select a product category to see recommendations:",
            options=top_categories,
            index=0
        )
        
        if selected_category:
            # Find categories frequently bought with selected category
            related_pairs = pair_counts[
                (pair_counts['category_1'] == selected_category) | 
                (pair_counts['category_2'] == selected_category)
            ].head(5)
            
            if not related_pairs.empty:
                st.markdown(f"**Customers who bought `{selected_category}` also bought:**")
                
                for _, row in related_pairs.iterrows():
                    rec_category = row['category_2'] if row['category_1'] == selected_category else row['category_1']
                    confidence = min(100, int((row['frequency'] / pair_counts['frequency'].max()) * 100))
                    
                    st.markdown(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(6,182,212,0.1));
                        border-left: 4px solid #6366f1;
                        padding: 1rem 1.5rem;
                        border-radius: 0 12px 12px 0;
                        margin-bottom: 0.8rem;
                    ">
                        <strong style="color: #6366f1; font-size: 1.1rem;">{rec_category}</strong>
                        <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.3rem;">
                            Confidence: {confidence}% | Co-purchased {row['frequency']} times
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"Not enough data for `{selected_category}` in current filter range.")
        
        # --- Section 4: Business Insight ---
        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); border-radius: 16px; padding: 1.5rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">📊 Business Insight</h4>
            <p style="color: #cbd5e1; margin: 0;">
                Cross-category recommendations can increase average order value by <strong>15-25%</strong>. 
                Use these insights for bundle pricing, email marketing, and homepage personalization.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>Built by <b>Varshini A S</b> | IIT Roorkee Data Science | GSSoC 2026</p>
            <p>📧 asvarshini84@gmail.com | 💼 Open for internships & freelance work</p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.info("Upload data files to 01_dataset/00_raw_data/ to get started")
