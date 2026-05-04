# Visualization Guide - Power BI and Tableau

This guide explains how to build a professional dashboard for the Customer Shopping Behavior Analysis project in both Power BI and Tableau.

## Dataset

Use:

```text
data/customer_shopping_behavior.csv
```

Recommended cleaned fields from Python/MySQL:

- `customer_id`
- `age`
- `gender`
- `item_purchased`
- `category`
- `purchase_amount`
- `location`
- `season`
- `review_rating`
- `subscription_status`
- `shipping_type`
- `discount_applied`
- `previous_purchases`
- `payment_method`
- `frequency_of_purchases`
- `age_group`
- `purchase_frequency_days`
- `estimated_annual_orders`
- `estimated_customer_lifetime_value`
- `rfm_segment`
- `churn_risk_flag`

If using the raw CSV directly, create calculated fields inside Power BI/Tableau for the engineered metrics listed below.

## Dashboard Goal

Help retail stakeholders understand revenue performance, customer value, customer segments, discount effectiveness, product performance, and retention opportunities.

## Dashboard Pages

### Page 1: Executive Overview

Purpose:
Give leadership a fast view of total performance and customer mix.

KPIs:

- Total Revenue
- Total Customers
- Average Order Value
- Average Review Rating
- Subscriber Rate
- Discount Usage Rate

Visuals:

- KPI cards: revenue, customers, AOV, subscriber rate
- Bar chart: revenue by gender
- Donut chart: revenue share by category
- Column chart: revenue by season
- Map: revenue by location
- Slicers: gender, age group, category, season, subscription status

Business question answered:
Where is revenue coming from, and which customer/product groups are driving the business?

### Page 2: Customer Segmentation and CLV

Purpose:
Identify high-value customers and customer segments for targeting.

KPIs:

- Average Estimated CLV
- Champion Customers
- At-Risk Customers
- Revenue from Champions

Visuals:

- Bar chart: average estimated CLV by RFM segment
- Matrix: RFM segment by age group with customers and revenue
- Scatter plot: previous purchases vs purchase amount, colored by RFM segment
- Table: top high-value non-subscribers

Business question answered:
Which customers deserve retention, loyalty, or subscription conversion campaigns?

### Page 3: Product and Seasonal Performance

Purpose:
Show category, item, and season performance for merchandising decisions.

KPIs:

- Top Category Revenue
- Top Item Revenue
- Highest Rated Category
- Highest Revenue Season

Visuals:

- Stacked column chart: revenue by category and season
- Treemap: item revenue by category
- Bar chart: top 10 items by revenue
- Heatmap/matrix: category by season with revenue and average rating

Business question answered:
Which products and seasons should receive campaign and inventory focus?

### Page 4: Discount, Churn, and Retention

Purpose:
Evaluate discount strategy and identify retention risk.

KPIs:

- Discounted Revenue
- Non-Discounted AOV
- Discounted AOV
- Churn-Risk Customers
- Revenue at Risk

Visuals:

- Clustered bar chart: discounted vs non-discounted revenue and AOV
- Bar chart: churn-risk customers by purchase frequency
- Table: high-CLV non-subscribers
- Matrix: RFM segment vs discount applied

Business question answered:
Are discounts helping, and which customers need retention action?

## Power BI Build Instructions

### Recommended Data Source

Use either:

- CSV from `data/customer_shopping_behavior.csv`
- MySQL table `customer_behavior.customer_data`

For the most complete dashboard, connect Power BI to MySQL after running the Python cleaning script or notebook.

### Power BI Measures

```DAX
Total Revenue =
SUM(customer_data[purchase_amount])

Customer Count =
DISTINCTCOUNT(customer_data[customer_id])

Average Order Value =
AVERAGE(customer_data[purchase_amount])

Average Review Rating =
AVERAGE(customer_data[review_rating])

Subscriber Customers =
CALCULATE(
    DISTINCTCOUNT(customer_data[customer_id]),
    customer_data[subscription_status] = "Yes"
)

Subscriber Rate =
DIVIDE([Subscriber Customers], [Customer Count])

Discounted Orders =
CALCULATE(
    COUNTROWS(customer_data),
    customer_data[discount_applied] = "Yes"
)

Discount Usage Rate =
DIVIDE([Discounted Orders], COUNTROWS(customer_data))

Estimated CLV =
SUMX(
    customer_data,
    customer_data[purchase_amount] *
    (
        customer_data[previous_purchases]
        + (365 / customer_data[purchase_frequency_days])
    )
)

Average Estimated CLV =
AVERAGEX(
    customer_data,
    customer_data[purchase_amount] *
    (
        customer_data[previous_purchases]
        + (365 / customer_data[purchase_frequency_days])
    )
)

Revenue at Risk =
CALCULATE(
    [Total Revenue],
    customer_data[churn_risk_flag] = 1
)
```

### Power BI Calculated Columns

```DAX
Age Group =
SWITCH(
    TRUE(),
    customer_data[age] <= 31, "Young Adult",
    customer_data[age] <= 44, "Adult",
    customer_data[age] <= 57, "Middle-aged",
    "Senior"
)

Purchase Frequency Days =
SWITCH(
    customer_data[frequency_of_purchases],
    "Weekly", 7,
    "Fortnightly", 14,
    "Bi-Weekly", 14,
    "Monthly", 30,
    "Quarterly", 90,
    "Every 3 Months", 90,
    "Annually", 365
)

Churn Risk Flag =
IF(
    customer_data[subscription_status] = "No"
        && customer_data[Purchase Frequency Days] >= 90
        && customer_data[previous_purchases] <= 25,
    1,
    0
)
```

### Design Style

- Use a clean retail analytics theme: white/light background, navy headings, green positive indicators, red risk indicators.
- Keep KPI cards at the top of each page.
- Use slicers on the left or top: gender, category, season, age group, subscription status.
- Add short chart titles that explain the business meaning, such as "Clothing Drives 44.7% of Revenue".

## Tableau Build Instructions

### Recommended Sheets

Create these Tableau sheets:

- KPI - Total Revenue
- KPI - Customer Count
- KPI - Average Order Value
- Revenue by Gender
- Revenue by Category
- Revenue by Season
- Revenue Map by Location
- CLV by Segment
- Previous Purchases vs Purchase Amount
- Discount Impact
- Churn Risk by Frequency
- Top High-Value Non-Subscribers

### Tableau Calculated Fields

```text
Total Revenue
SUM([purchase_amount])
```

```text
Average Order Value
AVG([purchase_amount])
```

```text
Subscriber Flag
IF [subscription_status] = "Yes" THEN 1 ELSE 0 END
```

```text
Subscriber Rate
AVG([Subscriber Flag])
```

```text
Discount Flag
IF [discount_applied] = "Yes" THEN 1 ELSE 0 END
```

```text
Purchase Frequency Days
CASE [frequency_of_purchases]
WHEN "Weekly" THEN 7
WHEN "Fortnightly" THEN 14
WHEN "Bi-Weekly" THEN 14
WHEN "Monthly" THEN 30
WHEN "Quarterly" THEN 90
WHEN "Every 3 Months" THEN 90
WHEN "Annually" THEN 365
END
```

```text
Estimated CLV
[purchase_amount] * ([previous_purchases] + (365 / [Purchase Frequency Days]))
```

```text
Churn Risk Flag
IF [subscription_status] = "No"
AND [Purchase Frequency Days] >= 90
AND [previous_purchases] <= 25
THEN "At Risk"
ELSE "Not At Risk"
END
```

### Tableau Dashboard Layout

Dashboard 1: Executive Overview

- Top row: KPI tiles
- Middle row: revenue by category and revenue by gender
- Bottom row: revenue by season and map by location

Dashboard 2: Customer Value and Retention

- Top row: average CLV and churn-risk KPI
- Middle row: CLV by segment and scatter plot
- Bottom row: high-value non-subscriber table

Dashboard 3: Product and Discount Strategy

- Top row: product/category KPIs
- Middle row: top items and seasonal category heatmap
- Bottom row: discount impact chart

## Storytelling Flow

Use this sequence when presenting:

1. Revenue is concentrated in specific categories and customer groups.
2. Customer value differs more by behavior than by one-time order amount.
3. Discounts are not strongly lifting AOV, so broad discounting is inefficient.
4. High-value non-subscribers and at-risk customers should be targeted with different campaigns.
5. The dashboard converts raw shopping behavior into retention, merchandising, and marketing decisions.
