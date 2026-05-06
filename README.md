# 🛒 Olist E-Commerce Analytics

An end-to-end analytics project built on the 
[Brazilian E-Commerce dataset (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

---

## 📊 Live Demo
🔗 https://olist-ecommerce-analytics-dusuawrhsjg7jgmojjnes9.streamlit.app/

---

## 🎯 Project Objectives
- Analyse revenue trends, customer behaviour and delivery performance
- Segment customers using RFM analysis
- Identify top revenue-driving product categories (Pareto)
- Build an interactive dashboard for business stakeholders

---

## 🔍 Key Business Insights

| Insight | Finding |
|---------|---------|
| 📈 Revenue Growth | 2,051% growth from first to last month |
| 🏆 Peak Month | November 2017 (Black Friday effect) |
| 👥 Customer Segments | Champions = highest LTV, 97% are one-time buyers |
| 📦 Pareto Rule | 17 categories drive 80% of total revenue |
| 🚚 Delivery Performance | 93.2% on-time rate, -0.45 correlation with reviews |
| 💳 Payment Behaviour | 78.3% credit card, instalment plans widely used |
| 🔁 Retention Problem | 97% one-time buyers → retention is #1 growth lever |

---

## 🛠️ Tools & Tech Stack

| Layer | Tools |
|-------|-------|
| Data Processing | Python (pandas, numpy) |
| Visualisation | Plotly, Power BI |
| Web App | Streamlit |
| Database | MySQL |
| Version Control | Git & GitHub |

---

## 📁 Project Structure
olist_analytics/
├── data/               ← Raw CSVs (not tracked)
├── notebooks/          ← Jupyter analysis notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_core_analysis.ipynb
│   └── 04_advanced_analysis.ipynb
├── scripts/            ← Python scripts
│   ├── kpi_definitions.py
│   └── business_insights.py
├── exports/            ← Cleaned & analysis-ready CSVs
├── app.py              ← Streamlit dashboard
└── README.md
---

## 📐 Analysis Performed

### Core Analysis
- **RFM Segmentation** — Ranked all customers by Recency, Frequency, Monetary value
- **Cohort Analysis** — Monthly retention matrix from first purchase
- **Time Series** — Revenue and order trends with MoM growth rates

### Advanced Analysis
- **Pareto Analysis** — 80/20 category revenue concentration
- **Customer LTV** — Bronze → Platinum tier segmentation
- **Delivery Performance** — On-time rates and delay impact on reviews
- **Payment Behaviour** — Payment type mix and instalment patterns
- **Repeat Purchase Rate** — One-time vs returning customer analysis

---

## 💡 Business Recommendations

1. **Retention Programme** — 97% one-time buyers signals huge opportunity.
   Post-purchase email sequences or loyalty rewards could significantly
   lift LTV.

2. **Logistics Improvement** — Delivery time has a -0.45 correlation with
   review scores. Improving fulfilment speed in slow states would
   directly increase customer satisfaction.

3. **Category Focus** — 17 categories drive 80% of revenue. Marketing and
   inventory investment should be concentrated here for maximum ROI.

4. **Champion Retention** — Champions are a small % of customers but
   generate disproportionate revenue. A VIP retention strategy is
   essential.

5. **Credit Card Promotions** — 78.3% of revenue via credit card with
   heavy instalment usage. 0% instalment promotions could boost
   conversion rates for high-ticket categories.

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/clyip08/olist-ecommerce-analytics.git

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py
```

---

## 👤 Author
**YIP CHEN LENG**
[https://www.linkedin.com/in/yipcl](#) | [GitHub](#)
