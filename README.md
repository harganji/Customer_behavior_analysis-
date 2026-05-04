# Customer Shopping Behavior Analysis

An end-to-end retail analytics project that turns raw customer shopping data into business recommendations using Python, MySQL, SQL analytics, customer segmentation, machine learning, and a Power BI dashboard design.

## Project Objective

Retail teams often know what customers purchased, but not which behaviors should drive retention, promotion, and merchandising decisions. This project analyzes customer shopping behavior to identify revenue drivers, estimate customer value, detect churn-risk signals, evaluate discount effectiveness, and recommend targeted business actions.

## Business Questions

- Which customer groups generate the most revenue?
- Which product categories and seasons should receive campaign focus?
- Which customers show high estimated lifetime value?
- Which customers are at risk of churn based on subscription status, purchase frequency, and purchase history?
- Do discounts improve customer value, or do they reduce margin without lifting order value?
- Which customer segments should receive loyalty, cross-sell, or win-back campaigns?

## Dataset

The dataset contains 3,900 customer shopping records with fields such as customer demographics, purchased item, category, purchase amount, location, season, review rating, subscription status, discount usage, previous purchases, payment method, and purchase frequency.

## Tools Used

- Python: data cleaning, feature engineering, EDA, correlation analysis, machine learning
- Pandas and NumPy: data transformation
- Scikit-learn: RandomForest classification and regression models
- MySQL: cleaned data storage and SQL analysis
- SQL: CTEs, window functions, RFM segmentation, cohort-style analysis
- Tableau: dashboard workbook starter and visual dashboard assets
- Power BI: dashboard structure and KPI design for future `.pbix` creation
- GitHub: portfolio documentation and project storytelling

Reference learning resource:
[YouTube - Customer Shopping Behavior Analysis walkthrough](https://www.youtube.com/watch?v=5PrZvPeUw60&t=1700s)

## Repository Structure

```text
customer-shopping-behavior-analysis/
  data/
    customer_shopping_behavior.csv
  sql/
    mysql_load_cleaned_data.sql
    advanced_customer_behavior_analysis.sql
  src/
    advanced_customer_analysis.py
  dashboard/
    power_bi_dashboard_blueprint.md
  docs/
    business_problem_and_story.md
    business_recommendations.md
    final_project_summary.md
  outputs/
    generated analysis outputs
  README.md
  requirements.txt
```

## Data Preparation

The Python workflow performs the following cleaning and transformation steps:

- Standardizes column names for SQL compatibility
- Imputes missing review ratings using category-level medians
- Removes duplicate promotional fields where discount and promo behavior are equivalent
- Creates age groups using quantiles
- Maps purchase frequency into estimated days between purchases
- Engineers estimated annual orders
- Creates an estimated customer lifetime value proxy
- Creates RFM scores and customer segments
- Flags churn-risk customers using behavioral rules

## Advanced Analytics

### SQL Analysis

The SQL analysis includes:

- Revenue by gender, category, season, location, and payment method
- Window functions for ranking categories, items, and locations
- RFM customer segmentation using NTILE
- CLV proxy analysis by age group and gender
- Discount impact analysis
- Churn-risk proxy analysis
- Cohort-style behavior by age group and purchase frequency
- Subscription conversion opportunity list

SQL file:
[sql/advanced_customer_behavior_analysis.sql](sql/advanced_customer_behavior_analysis.sql)

### Python Analysis

The Python analysis includes:

- Feature engineering
- Business summary tables
- Correlation matrix
- RFM segmentation
- Estimated CLV analysis
- RandomForest classifier for high-value customer prediction
- RandomForest regressor for purchase amount prediction

Python file:
[src/advanced_customer_analysis.py](src/advanced_customer_analysis.py)

## Key Findings

- Total revenue in the dataset is $233,081.
- Male customers generated $157,890 in revenue, while female customers generated $75,191.
- Clothing is the largest revenue category, generating $104,264.
- Accessories is the second-largest category and is a strong cross-sell opportunity.
- Subscribers have higher estimated CLV than non-subscribers, even though their average order value is similar.
- Discounted customers do not show a meaningful lift in average order value, which suggests discounts should be targeted rather than broad.
- Fall generated the highest seasonal revenue at $60,018.
- Power customers show the highest estimated CLV and should receive loyalty-focused campaigns.

## Business Recommendations

1. Target discounts only to at-risk and low-engagement customers.
   Broad discounting does not materially increase average order value, so offers should be used to reactivate or retain customers instead of subsidizing purchases that may already happen.

2. Convert high-value non-subscribers.
   Non-subscribers with strong purchase history should receive subscription offers tied to benefits such as free shipping, early access, or loyalty points.

3. Use Clothing as the revenue anchor and Accessories as the cross-sell engine.
   Clothing generates the most revenue, while Accessories offers a strong add-on path for basket expansion.

4. Build lifecycle campaigns around purchase frequency.
   Customers with quarterly or annual purchase patterns should receive reminders before their expected repurchase window.

5. Personalize campaigns by RFM segment.
   Champions should receive exclusive access, Loyal Growth customers should receive cross-sell and subscription offers, At Risk customers should receive win-back campaigns, and Low Engagement customers should receive low-cost reactivation tests.

## Dashboard and Visualization Work

For visualization, I created Tableau-ready dashboard assets and a visual dashboard preview for GitHub. I also included a complete Power BI dashboard plan with KPIs, DAX measures, and page structure. A `.pbix` file can be created from the included dataset and Power BI guide, but this repository currently focuses on the Tableau starter workbook and dashboard preview files.

The dashboard is designed as a four-page executive analytics product:

1. Executive Overview
   Revenue, customers, AOV, subscriber rate, category mix, gender revenue, seasonality, and location performance.

2. Customer Segmentation and CLV
   RFM segments, estimated CLV, top high-value customers, and customer quality by age group.

3. Product and Seasonal Performance
   Category revenue, top items, category-season heatmap, and product-level merchandising insights.

4. Discount, Churn, and Retention
   Discount impact, churn-risk customers, revenue at risk, and subscription conversion opportunities.

Dashboard blueprint:
[dashboard/power_bi_dashboard_blueprint.md](dashboard/power_bi_dashboard_blueprint.md)

Power BI and Tableau visualization guide:
[dashboard/visualization_guide_powerbi_tableau.md](dashboard/visualization_guide_powerbi_tableau.md)

Dashboard files included:

- [dashboard/customer_shopping_dashboard.png](dashboard/customer_shopping_dashboard.png)
- [dashboard/customer_shopping_dashboard.html](dashboard/customer_shopping_dashboard.html)
- [dashboard/customer_shopping_tableau_starter.twb](dashboard/customer_shopping_tableau_starter.twb)
- [dashboard/customer_shopping_dashboard_data.csv](dashboard/customer_shopping_dashboard_data.csv)
- [dashboard/power_bi_pbix_creation_steps.md](dashboard/power_bi_pbix_creation_steps.md)

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Python analysis:

```bash
python src/advanced_customer_analysis.py
```

Run the SQL analysis in MySQL Workbench after loading the cleaned data into:

```sql
customer_behavior.customer_data
```

## Interview Story

I started with a raw shopping behavior dataset and reframed it as a retail decision problem: how can the business increase customer value, reduce churn risk, and improve campaign targeting? I cleaned and engineered the data in Python, loaded it into MySQL, used SQL for business analysis and segmentation, created Tableau-ready visualization assets, planned a Power BI dashboard, and added a machine learning layer to predict high-value customers. The final output is not just an EDA notebook, but a business analytics project that connects analysis to action.

## Project Outcome

This project demonstrates the ability to move from data cleaning to executive insight. It shows technical depth through SQL window functions, Python feature engineering, segmentation, and ML, while also presenting findings in a business-ready format for decision-makers.
