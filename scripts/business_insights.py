import pandas as pd
import os

EXPORT_PATH = r"C:\Users\yipch\OneDrive\Desktop\olist_analytics\exports"

# ── Load all files ─────────────────────────────────────────────
master   = pd.read_csv(os.path.join(EXPORT_PATH, "final_master.csv"),
                       parse_dates=['order_purchase_timestamp'])
rfm      = pd.read_csv(os.path.join(EXPORT_PATH, "final_rfm.csv"))
monthly  = pd.read_csv(os.path.join(EXPORT_PATH, "final_monthly.csv"))
pareto   = pd.read_csv(os.path.join(EXPORT_PATH, "final_pareto.csv"))
delivery = pd.read_csv(os.path.join(EXPORT_PATH, "final_delivery.csv"))
payments = pd.read_csv(os.path.join(EXPORT_PATH, "final_payments.csv"))
ltv      = pd.read_csv(os.path.join(EXPORT_PATH, "final_ltv.csv"))

print("✅ All files loaded!\n")

# ══════════════════════════════════════════════════════════════
# INSIGHT 1 — REVENUE GROWTH
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("INSIGHT 1 — REVENUE GROWTH TREND")
print("=" * 60)

monthly_sorted = monthly.sort_values('order_year_month')
first_rev = monthly_sorted['revenue'].iloc[0]
peak_rev  = monthly_sorted['revenue'].max()
peak_mon  = monthly_sorted.loc[monthly_sorted['revenue'].idxmax(), 'order_year_month']
last_rev  = monthly_sorted['revenue'].iloc[-1]
growth    = ((last_rev - first_rev) / first_rev) * 100

print(f"• Peak revenue month : {peak_mon} — R$ {peak_rev:,.0f}")
print(f"• Overall growth     : {growth:.1f}% from first to last month")
print(f"• Best MoM growth    : {monthly_sorted['revenue_mom_pct'].max():.1f}%")
print()
print("💡 TALKING POINT:")
print(f"   'Revenue grew {growth:.0f}% over the dataset period,")
print(f"    peaking at R$ {peak_rev:,.0f} in {peak_mon}.'")

# ══════════════════════════════════════════════════════════════
# INSIGHT 2 — CUSTOMER SEGMENTS
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("INSIGHT 2 — CUSTOMER SEGMENTATION (RFM)")
print("=" * 60)

seg_summary = (master.groupby('segment')
               .agg(
                   customers     = ('customer_unique_id', 'nunique'),
                   total_revenue = ('total_revenue', 'sum'),
                   avg_order     = ('total_revenue', 'mean')
               )
               .reset_index()
               .sort_values('total_revenue', ascending=False))

total_customers = seg_summary['customers'].sum()
total_revenue   = seg_summary['total_revenue'].sum()

for _, row in seg_summary.iterrows():
    cust_pct = row['customers'] / total_customers * 100
    rev_pct  = row['total_revenue'] / total_revenue * 100
    print(f"  {row['segment']:<22} "
          f"Customers: {row['customers']:>6,} ({cust_pct:>5.1f}%)  "
          f"Revenue: R$ {row['total_revenue']:>12,.0f} ({rev_pct:>5.1f}%)")

champions = seg_summary[seg_summary['segment'] == 'Champions']
if not champions.empty:
    c_pct  = champions['customers'].values[0] / total_customers * 100
    rv_pct = champions['total_revenue'].values[0] / total_revenue * 100
    print()
    print("💡 TALKING POINT:")
    print(f"   'Champions make up only {c_pct:.1f}% of customers")
    print(f"    but contribute {rv_pct:.1f}% of total revenue —")
    print(f"    retaining this group is the #1 revenue priority.'")

# ══════════════════════════════════════════════════════════════
# INSIGHT 3 — PARETO (80/20)
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("INSIGHT 3 — PARETO ANALYSIS (80/20 RULE)")
print("=" * 60)

top80        = pareto[pareto['cumulative_pct'] <= 80]
top80_count  = len(top80)
total_cats   = len(pareto)
top3_cats    = pareto.head(3)['category'].tolist()
top3_rev_pct = pareto.head(3)['revenue_pct'].sum()

print(f"• {top80_count} out of {total_cats} categories drive 80% of revenue")
print(f"• Top 3 categories: {', '.join(top3_cats)}")
print(f"• Top 3 categories alone = {top3_rev_pct:.1f}% of total revenue")
print()
print("💡 TALKING POINT:")
print(f"   'Just {top80_count} product categories generate 80% of revenue.")
print(f"    The top 3 — {top3_cats[0]}, {top3_cats[1]}, {top3_cats[2]} —")
print(f"    account for {top3_rev_pct:.1f}% of sales.")
print(f"    Marketing and inventory should prioritise these.'")

# ══════════════════════════════════════════════════════════════
# INSIGHT 4 — DELIVERY PERFORMANCE
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("INSIGHT 4 — DELIVERY PERFORMANCE")
print("=" * 60)

on_time_rate  = (master['delivery_delay_days'] <= 0).mean() * 100
avg_del_days  = master['delivery_days'].mean()
worst_state   = delivery.sort_values('avg_delivery_days', ascending=False).iloc[0]
best_state    = delivery.sort_values('avg_delivery_days').iloc[0]
late_corr     = delivery[['avg_delivery_days','avg_review']].corr().iloc[0,1]

print(f"• On-time delivery rate : {on_time_rate:.1f}%")
print(f"• Avg delivery time     : {avg_del_days:.1f} days")
print(f"• Slowest state         : {worst_state['customer_state']} "
      f"({worst_state['avg_delivery_days']:.1f} days avg)")
print(f"• Fastest state         : {best_state['customer_state']} "
      f"({best_state['avg_delivery_days']:.1f} days avg)")
print(f"• Delivery vs Review    : {late_corr:.2f} correlation")
print()
print("💡 TALKING POINT:")
print(f"   'There is a {late_corr:.2f} correlation between delivery time")
print(f"    and review score. {worst_state['customer_state']} averages")
print(f"    {worst_state['avg_delivery_days']:.1f} days — nearly")
print(f"    {worst_state['avg_delivery_days']/best_state['avg_delivery_days']:.1f}x")
print(f"    slower than {best_state['customer_state']}.")
print(f"    Improving logistics in slow states directly lifts satisfaction.'")

# ══════════════════════════════════════════════════════════════
# INSIGHT 5 — PAYMENT BEHAVIOUR
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("INSIGHT 5 — PAYMENT BEHAVIOUR")
print("=" * 60)

top_pay     = payments.sort_values('total_value', ascending=False).iloc[0]
top_pay_pct = top_pay['value_pct']

print(f"• Dominant payment type : {top_pay['payment_type']} "
      f"({top_pay_pct:.1f}% of revenue)")

for _, row in payments.iterrows():
    print(f"  {row['payment_type']:<20} "
          f"R$ {row['total_value']:>12,.0f}  ({row['value_pct']:>5.1f}%)")

print()
print("💡 TALKING POINT:")
print(f"   '{top_pay['payment_type'].title()} dominates at {top_pay_pct:.1f}%")
print(f"    of all transactions. Instalment plans are widely used,")
print(f"    suggesting price sensitivity — promotions offering")
print(f"    0% instalment deals could boost conversion rates.'")

# ══════════════════════════════════════════════════════════════
# INSIGHT 6 — REPEAT PURCHASE & RETENTION
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("INSIGHT 6 — REPEAT PURCHASE & RETENTION")
print("=" * 60)

orders_per_cust = (master.groupby('customer_unique_id')['order_id']
                   .nunique())
repeat_rate  = (orders_per_cust > 1).mean() * 100
one_time     = (orders_per_cust == 1).mean() * 100
avg_orders   = orders_per_cust.mean()

print(f"• Repeat purchase rate : {repeat_rate:.1f}%")
print(f"• One-time buyers      : {one_time:.1f}%")
print(f"• Avg orders/customer  : {avg_orders:.2f}")
print()
print("💡 TALKING POINT:")
print(f"   '{one_time:.1f}% of customers only buy once.")
print(f"    A retention programme targeting one-time buyers —")
print(f"    such as post-purchase email sequences or loyalty rewards —")
print(f"    could significantly increase LTV and repeat revenue.'")

# ══════════════════════════════════════════════════════════════
# SAVE INSIGHTS SUMMARY
# ══════════════════════════════════════════════════════════════
insights = {
    'metric':  [
        'Peak Revenue Month',
        'Overall Revenue Growth %',
        'Categories Driving 80% Revenue',
        'On-Time Delivery Rate %',
        'Avg Delivery Days',
        'Delivery vs Review Correlation',
        'Repeat Purchase Rate %',
        'One-Time Buyer Rate %',
        'Top Payment Type',
        'Top Payment Type % Share'
    ],
    'value': [
        peak_mon,
        round(growth, 1),
        top80_count,
        round(on_time_rate, 1),
        round(avg_del_days, 1),
        round(late_corr, 2),
        round(repeat_rate, 1),
        round(one_time, 1),
        top_pay['payment_type'],
        round(top_pay_pct, 1)
    ]
}

pd.DataFrame(insights).to_csv(
    os.path.join(EXPORT_PATH, "business_insights_summary.csv"),
    index=False
)

print("\n" + "=" * 60)
print("✅ business_insights_summary.csv saved to exports/")
print("=" * 60)