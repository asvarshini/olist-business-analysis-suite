import streamlit as st
import pandas as pd
import plotly.express as px
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
    
    # KPI Cards
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
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Revenue", "📦 Orders", "👥 Customers"])
    
    # Tab 1: Revenue
    with tab1:
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
    
    # Tab 2: Orders
    with tab2:
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
    
    # Tab 3: Customers - FIXED SEGMENTATION
    with tab3:
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
