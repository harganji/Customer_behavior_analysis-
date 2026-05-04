from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_shopping_behavior.csv"
DASHBOARD_DIR = ROOT / "dashboard"
DASHBOARD_DIR.mkdir(exist_ok=True)


def clean_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Review Rating"] = df.groupby("Category")["Review Rating"].transform(
        lambda values: values.fillna(values.median())
    )
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(usd)", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.strip("_")
    )
    df = df.rename(columns={"purchase_amount_": "purchase_amount"})
    df["age_group"] = pd.qcut(
        df["age"], q=4, labels=["Young Adult", "Adult", "Middle-aged", "Senior"]
    ).astype(str)
    freq_days = {
        "Weekly": 7,
        "Fortnightly": 14,
        "Bi-Weekly": 14,
        "Monthly": 30,
        "Quarterly": 90,
        "Every 3 Months": 90,
        "Annually": 365,
    }
    df["purchase_frequency_days"] = df["frequency_of_purchases"].map(freq_days)
    df["estimated_annual_orders"] = (365 / df["purchase_frequency_days"]).round(2)
    df["estimated_customer_lifetime_value"] = (
        df["purchase_amount"] * (df["previous_purchases"] + df["estimated_annual_orders"])
    ).round(2)
    df["churn_risk_flag"] = (
        (df["subscription_status"] == "No")
        & (df["purchase_frequency_days"] >= 90)
        & (df["previous_purchases"] <= df["previous_purchases"].median())
    ).astype(int)
    return df


def write_twb(csv_path: Path, twb_path: Path) -> None:
    directory = escape(str(csv_path.parent))
    filename = escape(csv_path.name)
    xml = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook version='2024.1' source-build='2024.1.0'>
  <document-format-change-manifest />
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
  </preferences>
  <datasources>
    <datasource caption='Customer Shopping Dashboard Data' inline='true' name='customer_shopping_dashboard_data' version='2024.1'>
      <connection class='textscan' directory='{directory}' filename='{filename}' password='' server='' />
      <column caption='Customer ID' datatype='integer' name='[customer_id]' role='dimension' type='ordinal' />
      <column caption='Gender' datatype='string' name='[gender]' role='dimension' type='nominal' />
      <column caption='Category' datatype='string' name='[category]' role='dimension' type='nominal' />
      <column caption='Season' datatype='string' name='[season]' role='dimension' type='nominal' />
      <column caption='Location' datatype='string' name='[location]' role='dimension' type='nominal' />
      <column caption='RFM Segment' datatype='string' name='[rfm_segment]' role='dimension' type='nominal' />
      <column caption='Subscription Status' datatype='string' name='[subscription_status]' role='dimension' type='nominal' />
      <column caption='Purchase Amount' datatype='real' name='[purchase_amount]' role='measure' type='quantitative' />
      <column caption='Estimated CLV' datatype='real' name='[estimated_customer_lifetime_value]' role='measure' type='quantitative' />
      <column caption='Previous Purchases' datatype='integer' name='[previous_purchases]' role='measure' type='quantitative' />
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Open Data Source'>
      <table>
        <view>
          <datasources>
            <datasource caption='Customer Shopping Dashboard Data' name='customer_shopping_dashboard_data' />
          </datasources>
        </view>
      </table>
    </worksheet>
  </worksheets>
  <dashboards>
    <dashboard name='Customer Shopping Dashboard Starter'>
      <style />
      <zones />
    </dashboard>
  </dashboards>
</workbook>
"""
    twb_path.write_text(xml, encoding="utf-8")


def main() -> None:
    df = clean_data()
    csv_path = DASHBOARD_DIR / "customer_shopping_dashboard_data.csv"
    df.to_csv(csv_path, index=False)
    write_twb(csv_path, DASHBOARD_DIR / "customer_shopping_tableau_starter.twb")
    print("Created Customer Shopping dashboard CSV and Tableau TWB starter.")


if __name__ == "__main__":
    main()
