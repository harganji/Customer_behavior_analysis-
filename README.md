# Customer Shopping Behavior Analysis

End-to-end retail analytics project using Python, MySQL, advanced SQL, Tableau-ready dashboard assets, Power BI planning, customer segmentation, and machine learning.

## Portfolio Summary

This project analyzes 3,900 customer shopping records to identify revenue drivers, customer value patterns, churn-risk signals, discount effectiveness, and product/seasonal opportunities. The goal is to move beyond basic EDA and show how customer behavior data can support marketing, retention, merchandising, and executive decision-making.

## Business Problem

Retail teams often know what customers bought, but not which customers are most valuable, which behaviors indicate retention risk, or whether discounts are actually improving performance. This project answers those questions through data cleaning, SQL analysis, segmentation, dashboarding, and predictive modeling.

## Repository Structure

```text
Customer_behavior_analysis-/
  data/
  src/
  sql/
  dashboard/
  docs/
  outputs/
  README.md
  requirements.txt
```

## Key Questions Answered

- Which customer groups generate the most revenue?
- Which product categories and seasons should receive campaign focus?
- Which customers have stronger estimated lifetime value?
- Which customers are at risk because they are non-subscribers and purchase infrequently?
- Are discounts increasing customer quality or reducing margin without lifting order value?
- Which customer segments should receive loyalty, cross-sell, or win-back campaigns?

## Tools Used

- Python, Pandas, NumPy
- MySQL and advanced SQL
- Scikit-learn
- Tableau starter workbook and dashboard assets
- Power BI dashboard planning for future `.pbix` creation
- HTML dashboard preview for GitHub

## Files Included

| File | Purpose |
| --- | --- |
| [`data/customer_shopping_behavior.csv`](data/customer_shopping_behavior.csv) | Source dataset |
| [`src/advanced_customer_analysis.py`](src/advanced_customer_analysis.py) | Python cleaning, feature engineering, analysis, and ML |
| [`src/create_dashboard_visuals.py`](src/create_dashboard_visuals.py) | Generates dashboard PNG/HTML previews |
| [`src/create_bi_workbook_assets.py`](src/create_bi_workbook_assets.py) | Generates Tableau-ready workbook/data assets |
| [`sql/advanced_customer_behavior_analysis.sql`](sql/advanced_customer_behavior_analysis.sql) | Advanced SQL analysis queries |
| [`sql/mysql_load_cleaned_data.sql`](sql/mysql_load_cleaned_data.sql) | MySQL validation/loading helper |
| [`dashboard/customer_shopping_dashboard.png`](dashboard/customer_shopping_dashboard.png) | Dashboard image preview |
| [`dashboard/customer_shopping_dashboard.html`](dashboard/customer_shopping_dashboard.html) | Browser-viewable dashboard preview |
| [`dashboard/customer_shopping_tableau_starter.twb`](dashboard/customer_shopping_tableau_starter.twb) | Tableau starter workbook |
| [`dashboard/customer_shopping_dashboard_data.csv`](dashboard/customer_shopping_dashboard_data.csv) | Dashboard-ready cleaned data |
| [`dashboard/power_bi_dashboard_blueprint.md`](dashboard/power_bi_dashboard_blueprint.md) | Power BI dashboard design plan |
| [`dashboard/power_bi_pbix_creation_steps.md`](dashboard/power_bi_pbix_creation_steps.md) | Steps to create the `.pbix` in Power BI Desktop |
| [`dashboard/visualization_guide_powerbi_tableau.md`](dashboard/visualization_guide_powerbi_tableau.md) | Power BI/Tableau build guide |
| [`docs/business_problem_and_story.md`](docs/business_problem_and_story.md) | Business framing and story |
| [`docs/business_recommendations.md`](docs/business_recommendations.md) | Actionable recommendations |
| [`docs/final_project_summary.md`](docs/final_project_summary.md) | Interview-ready project summary |
| [`outputs/`](outputs/) | Generated analysis outputs |

## Data Preparation

The Python workflow performs these steps:

- Standardized column names for SQL compatibility
- Imputed missing review ratings using category-level medians
- Removed duplicate promotional fields where discount and promo usage were equivalent
- Created age groups using quantiles
- Mapped purchase frequency into estimated days between purchases
- Engineered estimated annual orders and estimated CLV
- Created RFM scores and customer segments
- Flagged churn-risk customers using behavioral rules

## Advanced SQL Analysis

The SQL work includes revenue analysis, window functions, RFM segmentation, CLV proxy analysis, discount impact, churn-risk analysis, cohort-style behavior, and subscription conversion opportunities.

## Python and Machine Learning

- RandomForest classifier for high-value customer prediction
- RandomForest regressor for purchase amount estimation
- High-value customer classifier ROC AUC: `0.884`
- Purchase amount model MAE: `$20.78`

## Dashboard and Visualization

This repository includes Tableau-ready dashboard assets and an HTML/PNG dashboard preview. A Power BI `.pbix` can be created from the included dashboard data and the Power BI guide, but the repository currently includes the Tableau starter workbook and visual preview files.

Dashboard preview files:

- [Customer Shopping Dashboard PNG](dashboard/customer_shopping_dashboard.png)
- [Customer Shopping Dashboard HTML](dashboard/customer_shopping_dashboard.html)
- [Tableau Starter Workbook](dashboard/customer_shopping_tableau_starter.twb)
- [Dashboard Data CSV](dashboard/customer_shopping_dashboard_data.csv)
- [Power BI PBIX Creation Steps](dashboard/power_bi_pbix_creation_steps.md)

## Key Findings

- Total revenue: `$233,081`
- Male customers generated `$157,890`; female customers generated `$75,191`
- Clothing is the largest revenue category at `$104,264`
- Accessories is the second-largest category and a strong cross-sell opportunity
- Subscribers show higher estimated CLV than non-subscribers despite similar AOV
- Discounted customers do not show a meaningful lift in AOV
- Fall generated the highest seasonal revenue at `$60,018`

## Business Recommendations

1. Target discounts only to at-risk and low-engagement customers instead of using blanket promotions.
2. Convert high-value non-subscribers with benefits such as free shipping, loyalty points, or early access.
3. Use Clothing as the revenue anchor and Accessories as the cross-sell category.
4. Build lifecycle campaigns around expected repurchase frequency.
5. Personalize messaging by RFM segment: Champions, Loyal Growth, At Risk, and Low Engagement.

## How to Run

```bash
pip install -r requirements.txt
python src/advanced_customer_analysis.py
```

Run the SQL analysis in MySQL Workbench after loading the cleaned data into:

```sql
customer_behavior.customer_data
```

## Interview Story

I started with raw customer shopping behavior data and reframed it as a retail decision problem: how can the business increase customer value, reduce churn risk, and improve campaign targeting? I cleaned and engineered the data in Python, loaded it into MySQL, used SQL for segmentation and business analysis, created Tableau-ready visualization assets, planned a Power BI dashboard, and added a machine learning layer to predict high-value customers.

The final output is a complete analytics case study that connects data preparation, SQL, Python, visualization, and business recommendations.
