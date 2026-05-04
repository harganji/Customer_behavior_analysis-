# Customer Shopping Behavior Analysis - Business Story

## Business Objective

Retail leadership wants to move beyond descriptive reporting and understand which customer groups create the most revenue, which behaviors indicate high future value, and where retention or discount strategy can improve profitability. The goal is to convert raw shopping behavior into customer strategy: who to prioritize, what to promote, where churn risk exists, and how marketing should personalize campaigns.

## Core Business Questions

1. Which gender, age group, category, and season generate the highest revenue?
2. Which customers appear most valuable based on estimated lifetime value?
3. Which customers are at risk because they are non-subscribers, buy infrequently, and have lower purchase history?
4. Are discounts increasing customer quality, or are they reducing margin without improving order value?
5. Which product categories and seasonal combinations deserve inventory and marketing focus?
6. Which customer segments should receive retention offers, loyalty perks, or subscription campaigns?

## Problem to Analysis to Insight to Impact

### Problem
The business has transactional shopping data but no clear segmentation framework. Marketing decisions are likely based on broad averages rather than customer value, purchase cadence, discount response, or product preference.

### Analysis
The project cleans the dataset, standardizes fields, engineers business features, loads the result into MySQL, and performs SQL plus Python analysis. RFM segmentation, CLV proxy scoring, churn-risk flagging, discount impact analysis, and machine learning are used to move the project from basic EDA to decision support.

### Insight
Revenue is concentrated in Clothing, while Accessories and Footwear show strong value potential. Subscribers have a higher estimated CLV than non-subscribers, despite similar average order values, which suggests retention value is driven more by frequency and previous purchase behavior than by one-time basket size. Discounts do not materially lift average order value, so discounting should be targeted rather than broad.

### Impact
The business can prioritize high-value non-subscribers for subscription conversion, reduce blanket discounting, invest in high-revenue categories during stronger seasons, and build customer-level targeting rules for retention and cross-sell campaigns.

## Key Metrics

- Total revenue
- Average order value
- Revenue share by segment
- Estimated customer lifetime value
- RFM segment
- Churn risk flag
- Discount usage rate
- Subscription conversion opportunity
- Category and seasonal performance

## Portfolio Positioning

This project demonstrates a full data analyst workflow:

- Python cleaning and feature engineering
- MySQL database loading and validation
- Advanced SQL analysis with CTEs and window functions
- Customer segmentation and CLV proxy modeling
- Machine learning for high-value customer classification
- Power BI dashboard planning
- Business recommendations written for stakeholders
