# Power BI Dashboard Blueprint

## Page 1: Executive Overview

Purpose:
Give leadership a one-page view of business performance and customer mix.

KPIs:
- Total Revenue
- Total Customers
- Average Order Value
- Average Review Rating
- Subscriber Rate
- Discount Usage Rate

Visuals:
- KPI cards for total revenue, customers, AOV, and subscriber rate
- Bar chart: revenue by gender
- Donut chart: revenue share by category
- Line or column chart: revenue by season
- Map or filled map: revenue by location

Business meaning:
This page answers where revenue is coming from and which customer groups dominate the business.

## Page 2: Customer Segmentation and CLV

Purpose:
Show which customers are most valuable and how customer quality differs by segment.

KPIs:
- Average Estimated CLV
- Champion Customers
- At-Risk Customers
- Revenue from Champions

Visuals:
- Matrix: RFM segment by age group with revenue and customer count
- Bar chart: average estimated CLV by segment
- Scatter plot: previous purchases vs. purchase amount, colored by RFM segment
- Table: top 25 high-value non-subscribers

Business meaning:
This page supports retention, loyalty, and customer prioritization decisions.

## Page 3: Product and Seasonal Performance

Purpose:
Identify which categories and items should receive merchandising and campaign focus.

KPIs:
- Top Category Revenue
- Top Item Revenue
- Highest Rated Category
- Seasonal Revenue Peak

Visuals:
- Stacked bar chart: category revenue by season
- Treemap: item revenue by category
- Bar chart: top 10 items by revenue
- Heatmap/matrix: category by season with revenue and average rating

Business meaning:
This page helps merchandising teams plan inventory, promotions, and seasonal campaigns.

## Page 4: Discount, Churn, and Retention

Purpose:
Evaluate whether promotions are improving customer value and where retention action is needed.

KPIs:
- Revenue from Discounted Orders
- Non-Discounted AOV
- Discounted AOV
- Churn-Risk Customers
- Revenue at Risk

Visuals:
- Clustered bar chart: discounted vs. non-discounted AOV and revenue
- Bar chart: churn-risk customers by frequency of purchases
- Table: high CLV non-subscribers to target
- Slicer panel: gender, age group, category, season, subscription status

Business meaning:
This page turns analysis into campaign actions: who to target, what offer to use, and which customer group needs attention.

## Suggested Data Model

Single-table model:
- customer_data as the fact table

Optional star schema for a more advanced portfolio version:
- fact_customer_purchase
- dim_customer
- dim_product
- dim_location
- dim_behavior

## Suggested DAX Measures

```DAX
Total Revenue = SUM(customer_data[purchase_amount])

Average Order Value = AVERAGE(customer_data[purchase_amount])

Customer Count = DISTINCTCOUNT(customer_data[customer_id])

Subscriber Rate =
DIVIDE(
    CALCULATE(DISTINCTCOUNT(customer_data[customer_id]), customer_data[subscription_status] = "Yes"),
    DISTINCTCOUNT(customer_data[customer_id])
)

Discount Usage Rate =
DIVIDE(
    CALCULATE(COUNTROWS(customer_data), customer_data[discount_applied] = "Yes"),
    COUNTROWS(customer_data)
)

Estimated CLV =
SUMX(
    customer_data,
    customer_data[purchase_amount] *
    (customer_data[previous_purchases] + (365 / customer_data[purchase_frequency_days]))
)
```
