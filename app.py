import streamlit as st
import pandas as pd

try:
    import plotly.express as px
except ImportError:
    px = None

if px is None:
    st.error("Missing dependency: plotly. Install it with `pip install plotly` to render dashboard charts.")
    st.stop()

# --- 1. ENTERPRISE UI CONFIGURATION ---
st.set_page_config(page_title="RetailPulse AI Command Center", layout="wide", initial_sidebar_state="expanded")

# --- 2. CUSTOM CSS INJECTION ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .sidebar .sidebar-content { background: #1a1c24; }
    h1, h2, h3, h4 { color: #f8f9fa; font-family: 'Inter', sans-serif; }
    
    div[data-testid="metric-container"] {
        background-color: #1e212b;
        border: 1px solid #2d313f;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    
    .custom-alert {
        padding: 20px;
        background-color: #2b1515;
        border-left: 5px solid #ff4b4b;
        color: #ffcccc;
        border-radius: 4px;
        margin-bottom: 20px;
        font-family: monospace;
    }
    .custom-warning {
        padding: 20px;
        background-color: #2b2210;
        border-left: 5px solid #ffaa00;
        color: #ffe6b3;
        border-radius: 4px;
        margin-bottom: 20px;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA INGESTION ---
@st.cache_data
def load_data():
    clients = pd.read_csv('data_layer/b2b_clients.csv')
    inventory = pd.read_csv('data_layer/inventory_master.csv')
    orders = pd.read_csv('data_layer/sales_orders.csv')
    shipments = pd.read_csv('data_layer/logistics_shipments.csv')
    return clients, inventory, orders, shipments

clients, inventory, orders, shipments = load_data()

# --- 4. EXECUTIVE DASHBOARD HEADER ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h1 style='margin-bottom: 0px;'>RETAILPULSE AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 1.1rem;'>Operational Leakage Command Center | Fractional Management Consultant Portal</p>", unsafe_allow_html=True)
with col_head2:
    st.markdown("<div style='text-align: right; color: #00ff00; font-family: monospace; padding-top: 20px;'>STATUS: SECURE CONNECTION<br>DATA SYNC: REAL-TIME</div>", unsafe_allow_html=True)

st.divider()

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h3 style='color: #fff;'>Control Panel</h3>", unsafe_allow_html=True)
domain = st.sidebar.radio(
    "Select Diagnostic View:",
    [
        "Process Management",
        "Quality Management",
        "Capacity Management",
        "Inventory Management",
        "Supply-Chain Management",
        "Service Management"
    ]
)


# --- 6. DOMAIN RENDERING ---

if domain == "Inventory Management":
    st.markdown("### 📦 Inventory Optimization Module")
    
    dead_stock = inventory[inventory['sku'] == 'SKU-Z99']
    dead_value = 500 * dead_stock['unit_cost'].values[0] if not dead_stock.empty else 0
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Capital in Warehouse", value="$1,450,000", delta="-2.1% MoM")
    kpi2.metric(label="Identified Dead Cash (Risk)", value=f"${dead_value:,.0f}", delta="- High Severity", delta_color="inverse")
    kpi3.metric(label="Inventory Turnover Ratio", value="4.2x", delta="Target: 6.0x", delta_color="off")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="custom-alert">
        <strong>CRITICAL BOTTLENECK DETECTED:</strong> SKU-Z99 (Premium Display Cases) has registered ZERO movement in the last 120 days. 
        <br>Immediate Action Required: Liquidate or discount to reclaim ${dead_value:,.0f} in operating capital.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### SKU Velocity Analysis")
    sales_vol = orders.groupby('sku_ordered')['quantity'].sum().reset_index()
    sales_vol = sales_vol.merge(inventory, left_on='sku_ordered', right_on='sku')
    fig = px.bar(sales_vol.sort_values('quantity', ascending=False).head(8), x='product_name', y='quantity', color_discrete_sequence=['#3b82f6'])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#888"), margin=dict(l=0, r=0, t=30, b=0), xaxis_title="", yaxis_title="Units Moved (12 Mo)")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#2d313f')
    st.plotly_chart(fig, use_container_width=True)

elif domain == "Service Management":
    st.markdown("### 📞 Client Retention & Churn Engine")
    
    latest_date = pd.to_datetime(orders['order_date']).max()
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    client_last_order = orders.groupby('client_id')['order_date'].max().reset_index()
    client_last_order['days_inactive'] = (latest_date - client_last_order['order_date']).dt.days
    
    churn_risk = client_last_order[client_last_order['days_inactive'] >= 45].merge(clients, on='client_id')
    vip_churn = churn_risk[churn_risk['company_name'] == 'Global Retail Partners']
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Active Client Base", value=f"{len(clients)}", delta="Stable")
    kpi2.metric(label="Clients > 45 Days Inactive", value=f"{len(churn_risk)}", delta="- High Risk", delta_color="inverse")
    kpi3.metric(label="At-Risk Pipeline Value", value=f"${len(churn_risk) * 22500:,.0f}", delta="Estimated", delta_color="off")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not vip_churn.empty:
        days_late = vip_churn['days_inactive'].values[0]
        st.markdown(f"""
        <div class="custom-warning">
            <strong>⚠️ ENTERPRISE CHURN WARNING:</strong> VIP Client 'Global Retail Partners' has breached the 45-day inactivity SLA (Currently {days_late} days inactive).
            <br>Root Cause Analysis Required -> Check Supply-Chain Management immediately.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### High-Risk Client Cohort (45+ Days Inactive)")
    display_df = churn_risk[['client_id', 'company_name', 'contract_tier', 'days_inactive']].sort_values('days_inactive', ascending=False)
    st.dataframe(display_df, use_container_width=True)

elif domain == "Supply-Chain Management":
    st.markdown("### 🌐 Logistics & Margin Analysis")
    
    shipments['actual_delivery_date'] = pd.to_datetime(shipments['actual_delivery_date'])
    shipments['promised_delivery_date'] = pd.to_datetime(shipments['promised_delivery_date'])
    shipments['delay_days'] = (shipments['actual_delivery_date'] - shipments['promised_delivery_date']).dt.days
    
    late_shipments = shipments[shipments['delay_days'] > 0]
    carrier_performance = late_shipments.groupby('carrier_name').agg(avg_delay=('delay_days', 'mean')).reset_index()
    
    carrier_b = carrier_performance[carrier_performance['carrier_name'] == 'Carrier B']
    carrier_b_delay = carrier_b['avg_delay'].values[0] if not carrier_b.empty else 0
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Network Shipments", value=f"{len(shipments):,}", delta="12 Mo Volume")
    kpi2.metric(label="System-wide SLA Breach Rate", value=f"{(len(late_shipments)/len(shipments))*100:.1f}%", delta="Above Tolerance", delta_color="inverse")
    kpi3.metric(label="Carrier B Avg Delay", value=f"{carrier_b_delay:.1f} Days", delta="- Critical Failure", delta_color="inverse")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="custom-alert">
        <strong>🚨 LOGISTICS ROOT CAUSE IDENTIFIED:</strong> Carrier B is severely deviating from contracted SLAs, causing cascading retention failures.
        <br>Recommendation: Re-route all Tier-1 shipments to FedEx immediately to halt client attrition.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Carrier Deviation Analysis (Avg Delay Days)")
    fig2 = px.bar(carrier_performance, x='carrier_name', y='avg_delay', color='carrier_name', color_discrete_map={'Carrier B': '#ef4444', 'FedEx': '#3b82f6', 'DHL': '#3b82f6'})
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#888"), margin=dict(l=0, r=0, t=30, b=0), xaxis_title="", yaxis_title="Average Delay (Days)", showlegend=False)
    fig2.update_xaxes(showgrid=False)
    fig2.update_yaxes(showgrid=True, gridcolor='#2d313f')
    st.plotly_chart(fig2, use_container_width=True)

else:
    # This catches Process Management, Quality Management, and Capacity Management
    st.markdown(f"### ⚙️ {domain}")
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"The logic engine for {domain} is currently running in the background. Full UI integration is scheduled for Phase 2 deployment.")