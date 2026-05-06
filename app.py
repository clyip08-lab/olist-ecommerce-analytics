import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ── CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

EXPORT_PATH = os.path.join(os.path.dirname(__file__), "exports")

# ── LOAD DATA ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    master   = pd.read_csv(os.path.join(EXPORT_PATH, "final_master.csv"),
                           parse_dates=['order_purchase_timestamp'])
    rfm      = pd.read_csv(os.path.join(EXPORT_PATH, "final_rfm.csv"))
    monthly  = pd.read_csv(os.path.join(EXPORT_PATH, "final_monthly.csv"))
    pareto   = pd.read_csv(os.path.join(EXPORT_PATH, "final_pareto.csv"))
    delivery = pd.read_csv(os.path.join(EXPORT_PATH, "final_delivery.csv"))
    payments = pd.read_csv(os.path.join(EXPORT_PATH, "final_payments.csv"))
    dow      = pd.read_csv(os.path.join(EXPORT_PATH, "final_dow.csv"))
    return master, rfm, monthly, pareto, delivery, payments, dow

master, rfm, monthly, pareto, delivery, payments, dow = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/shopping-cart.png", width=80)
st.sidebar.title("Olist Analytics")
st.sidebar.markdown("**Brazilian E-Commerce**")
st.sidebar.markdown("---")

page = st.sidebar.radio("📄 Navigate", [
    "🏠 Executive Overview",
    "👥 Customer Segments",
    "📦 Product & Payment",
    "🚚 Delivery Performance"
])

months   = sorted(master['order_year_month'].dropna().unique())
selected = st.sidebar.select_slider(
    "📅 Filter by Month Range",
    options=months,
    value=(months[0], months[-1])
)

mask     = (
    (master['order_year_month'] >= selected[0]) &
    (master['order_year_month'] <= selected[1])
)
filtered = master[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing:** {selected[0]} → {selected[1]}")
st.sidebar.markdown(f"**Orders:** {filtered['order_id'].nunique():,}")

# ══════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "🏠 Executive Overview":
    st.title("🏠 Executive Overview")
    st.markdown("High-level business performance at a glance.")
    st.markdown("---")

    total_rev = filtered['total_revenue'].sum()
    total_ord = filtered['order_id'].nunique()

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("💰 Total Revenue", f"R$ {total_rev:,.0f}")
    k2.metric("📦 Total Orders",  f"{total_ord:,}")
    k3.metric("👥 Customers",     f"{filtered['customer_unique_id'].nunique():,}")
    k4.metric("🛒 AOV",           f"R$ {total_rev / total_ord:,.2f}")
    k5.metric("⭐ Avg Review",    f"{filtered['review_score'].mean():.2f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        monthly_f = monthly[
            (monthly['order_year_month'] >= selected[0]) &
            (monthly['order_year_month'] <= selected[1])
        ].copy()

        fig_rev = px.line(
            monthly_f,
            x='order_year_month',
            y='revenue',
            title='📅 Monthly Revenue Trend',
            markers=True,
            labels={'order_year_month': 'Month', 'revenue': 'Revenue (R$)'}
        )
        fig_rev.update_traces(line_color='#2563EB', line_width=2.5)
        st.plotly_chart(fig_rev, use_container_width=True, key="p1_revenue_trend")

    with col2:
        dow_order  = ['Monday','Tuesday','Wednesday',
                      'Thursday','Friday','Saturday','Sunday']
        dow_sorted = dow.set_index('order_dow').reindex(dow_order).reset_index()

        fig_dow = px.bar(
            dow_sorted,
            x='orders',
            y='order_dow',
            orientation='h',
            title='📅 Orders by Day of Week',
            labels={'order_dow': 'Day', 'orders': 'Orders'},
            color='orders',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_dow, use_container_width=True, key="p1_dow")

    with st.expander("📊 View Monthly Data Table"):
        st.dataframe(
            monthly_f.style.format({
                'revenue':         'R$ {:,.2f}',
                'orders':          '{:,}',
                'customers':       '{:,}',
                'revenue_mom_pct': '{:.1f}%'
            }),
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════
# PAGE 2 — CUSTOMER SEGMENTS
# ══════════════════════════════════════════════════════════════
elif page == "👥 Customer Segments":
    st.title("👥 Customer Segments (RFM)")
    st.markdown("Customers ranked by Recency, Frequency & Monetary value.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        seg_counts = filtered['segment'].value_counts().reset_index()
        seg_counts.columns = ['segment', 'count']

        fig_pie = px.pie(
            seg_counts,
            names='segment',
            values='count',
            hole=0.45,
            title='🧩 Customer Segment Distribution',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="p2_seg_pie")

    with col2:
        seg_rev = (
            filtered.groupby('segment')['total_revenue']
            .sum()
            .reset_index()
            .sort_values('total_revenue', ascending=True)
        )

        fig_seg_rev = px.bar(
            seg_rev,
            x='total_revenue',
            y='segment',
            orientation='h',
            title='💰 Revenue by Segment',
            labels={'total_revenue': 'Revenue (R$)', 'segment': 'Segment'},
            color='total_revenue',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_seg_rev, use_container_width=True, key="p2_seg_rev")

    st.markdown("### 📊 Segment Summary Table")
    seg_table = (
        filtered.groupby('segment')
        .agg(
            customers     = ('customer_unique_id', 'nunique'),
            total_revenue = ('total_revenue', 'sum'),
            avg_revenue   = ('total_revenue', 'mean'),
            avg_review    = ('review_score', 'mean')
        )
        .reset_index()
        .round(2)
        .sort_values('total_revenue', ascending=False)
    )
    st.dataframe(seg_table, use_container_width=True)

    st.markdown("### 🎯 RFM Score Distribution")
    fig_rfm = px.scatter(
        rfm,
        x='recency',
        y='monetary',
        color='segment',
        size='frequency',
        title='Recency vs Monetary (bubble = Frequency)',
        labels={'recency': 'Recency (days)', 'monetary': 'Monetary (R$)'},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_rfm, use_container_width=True, key="p2_rfm_scatter")

# ══════════════════════════════════════════════════════════════
# PAGE 3 — PRODUCT & PAYMENT
# ══════════════════════════════════════════════════════════════
elif page == "📦 Product & Payment":
    st.title("📦 Product & Payment Analysis")
    st.markdown("Category revenue breakdown and payment behaviour.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        top20 = pareto.head(20).copy()

        fig_cat = px.bar(
            top20.sort_values('revenue'),
            x='revenue',
            y='category',
            orientation='h',
            title='📦 Top 20 Categories by Revenue',
            labels={'revenue': 'Revenue (R$)', 'category': 'Category'},
            color='revenue',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_cat, use_container_width=True, key="p3_cat_bar")

    with col2:
        fig_pay = px.pie(
            payments,
            names='payment_type',
            values='total_value',
            hole=0.45,
            title='💳 Revenue by Payment Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pay, use_container_width=True, key="p3_pay_pie")

    st.markdown("### 📈 Pareto Chart — Cumulative Revenue %")
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(
        x=pareto['category'].head(30),
        y=pareto['revenue'].head(30),
        name='Revenue',
        marker_color='#2563EB'
    ))
    fig_pareto.add_trace(go.Scatter(
        x=pareto['category'].head(30),
        y=pareto['cumulative_pct'].head(30),
        name='Cumulative %',
        yaxis='y2',
        line=dict(color='orange', width=2.5)
    ))
    fig_pareto.update_layout(
        yaxis2=dict(
            overlaying='y', side='right',
            range=[0, 105], title='Cumulative %'
        ),
        yaxis=dict(title='Revenue (R$)'),
        xaxis_tickangle=-45,
        legend=dict(x=0.7, y=0.2)
    )
    st.plotly_chart(fig_pareto, use_container_width=True, key="p3_pareto_line")

# ══════════════════════════════════════════════════════════════
# PAGE 4 — DELIVERY PERFORMANCE
# ══════════════════════════════════════════════════════════════
elif page == "🚚 Delivery Performance":
    st.title("🚚 Delivery Performance")
    st.markdown("Delivery speed, delays, and impact on customer satisfaction.")
    st.markdown("---")

    on_time = (filtered['delivery_delay_days'] <= 0).mean() * 100

    d1, d2, d3 = st.columns(3)
    d1.metric("✅ On-Time Rate", f"{on_time:.1f}%")
    d2.metric("📦 Avg Delivery", f"{filtered['delivery_days'].mean():.1f} days")
    d3.metric("⚠️ Avg Delay",    f"{filtered['delivery_delay_days'].mean():.1f} days")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        fig_del = px.bar(
            delivery.sort_values('avg_delivery_days', ascending=False).head(15),
            x='avg_delivery_days',
            y='customer_state',
            orientation='h',
            title='Avg Delivery Days by State',
            labels={'avg_delivery_days': 'Avg Days', 'customer_state': 'State'},
            color='avg_delivery_days',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_del, use_container_width=True, key="p4_del_bar")

    with col2:
        fig_scatter = px.scatter(
            delivery,
            x='avg_delivery_days',
            y='avg_review',
            text='customer_state',
            size='total_orders',
            title='Delivery Time vs Review Score',
            labels={
                'avg_delivery_days': 'Avg Delivery Days',
                'avg_review': 'Avg Review Score'
            },
            color='avg_review',
            color_continuous_scale='RdYlGn'
        )
        fig_scatter.update_traces(textposition='top center')
        st.plotly_chart(fig_scatter, use_container_width=True, key="p4_del_scatter")

    st.markdown("### ⚠️ Late Delivery Rate by State")
    fig_late = px.bar(
        delivery.sort_values('late_rate_pct', ascending=False),
        x='customer_state',
        y='late_rate_pct',
        title='Late Delivery Rate by State',
        labels={'late_rate_pct': 'Late Rate %', 'customer_state': 'State'},
        color='late_rate_pct',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_late, use_container_width=True, key="p4_late_bar")

    with st.expander("📊 Full Delivery Table"):
        st.dataframe(
            delivery.sort_values('avg_delivery_days', ascending=False),
            use_container_width=True
        )