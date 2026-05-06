import pandas as pd
import os

EXPORT_PATH = r"C:\Users\yipch\OneDrive\Desktop\olist_analytics\exports"

# ── Load master table ──────────────────────────────────────────
master = pd.read_csv(os.path.join(EXPORT_PATH, "master_orders.csv"),
                     parse_dates=['order_purchase_timestamp',
                                  'order_delivered_customer_date',
                                  'order_estimated_delivery_date'])

print(f"✅ Master loaded: {master.shape}")

# ══════════════════════════════════════════════════════════════
# KPI 1 — Total Revenue
# Definition: Sum of item prices (excluding freight)
# ══════════════════════════════════════════════════════════════
total_revenue = master['total_revenue'].sum()
print(f"\n💰 KPI 1 | Total Revenue:        R$ {total_revenue:,.2f}")

# ══════════════════════════════════════════════════════════════
# KPI 2 — Total Orders
# Definition: Count of unique delivered orders
# ══════════════════════════════════════════════════════════════
total_orders = master['order_id'].nunique()
print(f"📦 KPI 2 | Total Orders:          {total_orders:,}")

# ══════════════════════════════════════════════════════════════
# KPI 3 — Total Unique Customers
# Definition: Count of unique customer_unique_id
# ══════════════════════════════════════════════════════════════
total_customers = master['customer_unique_id'].nunique()
print(f"👥 KPI 3 | Total Customers:       {total_customers:,}")

# ══════════════════════════════════════════════════════════════
# KPI 4 — Average Order Value (AOV)
# Definition: Total Revenue ÷ Total Orders
# ══════════════════════════════════════════════════════════════
aov = total_revenue / total_orders
print(f"🛒 KPI 4 | Avg Order Value (AOV): R$ {aov:,.2f}")

# ══════════════════════════════════════════════════════════════
# KPI 5 — Average Review Score
# Definition: Mean of all review scores (1–5)
# ══════════════════════════════════════════════════════════════
avg_review = master['review_score'].mean()
print(f"⭐ KPI 5 | Avg Review Score:      {avg_review:.2f} / 5.00")

# ══════════════════════════════════════════════════════════════
# KPI 6 — Average Delivery Time
# Definition: Mean days from purchase to delivery
# ══════════════════════════════════════════════════════════════
avg_delivery = master['delivery_days'].mean()
print(f"🚚 KPI 6 | Avg Delivery Days:     {avg_delivery:.1f} days")

# ══════════════════════════════════════════════════════════════
# KPI 7 — On-Time Delivery Rate
# Definition: % of orders delivered on or before estimated date
# ══════════════════════════════════════════════════════════════
on_time = (master['delivery_delay_days'] <= 0).sum()
on_time_rate = on_time / total_orders * 100
print(f"✅ KPI 7 | On-Time Delivery Rate: {on_time_rate:.1f}%")

# ══════════════════════════════════════════════════════════════
# KPI 8 — Repeat Purchase Rate
# Definition: % of customers who placed more than 1 order
# ══════════════════════════════════════════════════════════════
orders_per_customer = master.groupby('customer_unique_id')['order_id'].nunique()
repeat_customers    = (orders_per_customer > 1).sum()
repeat_rate         = repeat_customers / total_customers * 100
print(f"🔁 KPI 8 | Repeat Purchase Rate:  {repeat_rate:.1f}%")

# ══════════════════════════════════════════════════════════════
# KPI 9 — Revenue per Customer
# Definition: Total Revenue ÷ Total Unique Customers
# ══════════════════════════════════════════════════════════════
rev_per_customer = total_revenue / total_customers
print(f"💵 KPI 9 | Revenue per Customer:  R$ {rev_per_customer:,.2f}")

# ══════════════════════════════════════════════════════════════
# KPI 10 — Monthly Revenue Table
# Definition: Revenue grouped by YYYY-MM
# ══════════════════════════════════════════════════════════════
monthly_revenue = (
    master.groupby('order_year_month')['total_revenue']
    .sum()
    .reset_index()
    .rename(columns={'order_year_month': 'month', 'total_revenue': 'revenue'})
    .sort_values('month')
)

print(f"\n📅 KPI 10 | Monthly Revenue (last 6 months):")
print(monthly_revenue.tail(6).to_string(index=False))

# ══════════════════════════════════════════════════════════════
# SAVE KPI SUMMARY
# ══════════════════════════════════════════════════════════════
kpi_summary = pd.DataFrame([{
    'total_revenue':      round(total_revenue, 2),
    'total_orders':       total_orders,
    'total_customers':    total_customers,
    'aov':                round(aov, 2),
    'avg_review_score':   round(avg_review, 2),
    'avg_delivery_days':  round(avg_delivery, 1),
    'on_time_rate_pct':   round(on_time_rate, 1),
    'repeat_rate_pct':    round(repeat_rate, 1),
    'rev_per_customer':   round(rev_per_customer, 2)
}])

kpi_summary.to_csv(os.path.join(EXPORT_PATH, "kpi_summary.csv"), index=False)
monthly_revenue.to_csv(os.path.join(EXPORT_PATH, "monthly_revenue.csv"), index=False)

print("\n✅ kpi_summary.csv and monthly_revenue.csv saved to exports/")