from pathlib import Path

import matplotlib.pyplot as plt
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

    frequency_days = {
        "Weekly": 7,
        "Fortnightly": 14,
        "Bi-Weekly": 14,
        "Monthly": 30,
        "Quarterly": 90,
        "Every 3 Months": 90,
        "Annually": 365,
    }
    df["purchase_frequency_days"] = df["frequency_of_purchases"].map(frequency_days)
    df["estimated_clv"] = (
        df["purchase_amount"]
        * (df["previous_purchases"] + (365 / df["purchase_frequency_days"]))
    )
    df["churn_risk_flag"] = (
        (df["subscription_status"] == "No")
        & (df["purchase_frequency_days"] >= 90)
        & (df["previous_purchases"] <= df["previous_purchases"].median())
    )
    return df


def add_bar_labels(ax, fmt="{:,.0f}"):
    for container in ax.containers:
        ax.bar_label(container, labels=[fmt.format(v.get_height()) for v in container], fontsize=8)


def create_png_dashboard(df: pd.DataFrame) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Customer Shopping Behavior Analysis Dashboard", fontsize=22, fontweight="bold")

    total_revenue = df["purchase_amount"].sum()
    customers = df["customer_id"].nunique()
    aov = df["purchase_amount"].mean()
    churn_risk = int(df["churn_risk_flag"].sum())

    ax0 = fig.add_subplot(3, 4, 1)
    ax0.axis("off")
    ax0.text(0, 0.82, "Total Revenue", fontsize=12, color="#555")
    ax0.text(0, 0.62, f"${total_revenue:,.0f}", fontsize=24, fontweight="bold")
    ax0.text(0, 0.40, "Customers", fontsize=12, color="#555")
    ax0.text(0, 0.24, f"{customers:,.0f}", fontsize=22, fontweight="bold")
    ax0.text(0, 0.06, f"AOV: ${aov:,.2f} | Churn Risk: {churn_risk}", fontsize=11)

    ax1 = fig.add_subplot(3, 4, 2)
    gender_rev = df.groupby("gender")["purchase_amount"].sum().sort_values(ascending=False)
    gender_rev.plot(kind="bar", ax=ax1, color=["#2f6f9f", "#f28e2b"])
    ax1.set_title("Revenue by Gender")
    ax1.set_xlabel("")
    ax1.set_ylabel("Revenue")
    add_bar_labels(ax1, "${:,.0f}")

    ax2 = fig.add_subplot(3, 4, 3)
    category_rev = df.groupby("category")["purchase_amount"].sum().sort_values(ascending=False)
    category_rev.plot(kind="bar", ax=ax2, color="#59a14f")
    ax2.set_title("Revenue by Category")
    ax2.set_xlabel("")
    ax2.set_ylabel("Revenue")

    ax3 = fig.add_subplot(3, 4, 4)
    season_rev = df.groupby("season")["purchase_amount"].sum().sort_values(ascending=False)
    season_rev.plot(kind="bar", ax=ax3, color="#e15759")
    ax3.set_title("Revenue by Season")
    ax3.set_xlabel("")
    ax3.set_ylabel("Revenue")

    ax4 = fig.add_subplot(3, 4, 5)
    top_items = df.groupby("item_purchased")["purchase_amount"].sum().nlargest(8).sort_values()
    top_items.plot(kind="barh", ax=ax4, color="#76b7b2")
    ax4.set_title("Top Items by Revenue")
    ax4.set_xlabel("Revenue")

    ax5 = fig.add_subplot(3, 4, 6)
    discount_aov = df.groupby("discount_applied")["purchase_amount"].mean()
    discount_aov.plot(kind="bar", ax=ax5, color=["#4e79a7", "#edc948"])
    ax5.set_title("Average Order Value by Discount")
    ax5.set_xlabel("Discount Applied")
    ax5.set_ylabel("AOV")
    add_bar_labels(ax5, "${:,.2f}")

    ax6 = fig.add_subplot(3, 4, 7)
    sub_clv = df.groupby("subscription_status")["estimated_clv"].mean()
    sub_clv.plot(kind="bar", ax=ax6, color=["#af7aa1", "#ff9da7"])
    ax6.set_title("Estimated CLV by Subscription")
    ax6.set_xlabel("Subscriber")
    ax6.set_ylabel("Avg Estimated CLV")

    ax7 = fig.add_subplot(3, 4, 8)
    freq_count = df.groupby("frequency_of_purchases")["customer_id"].count().sort_values()
    freq_count.plot(kind="barh", ax=ax7, color="#9c755f")
    ax7.set_title("Customers by Purchase Frequency")
    ax7.set_xlabel("Customers")

    ax8 = fig.add_subplot(3, 2, 5)
    scatter = ax8.scatter(
        df["previous_purchases"],
        df["purchase_amount"],
        c=df["estimated_clv"],
        cmap="viridis",
        alpha=0.65,
        s=28,
    )
    ax8.set_title("Previous Purchases vs Purchase Amount")
    ax8.set_xlabel("Previous Purchases")
    ax8.set_ylabel("Purchase Amount")
    fig.colorbar(scatter, ax=ax8, label="Estimated CLV")

    ax9 = fig.add_subplot(3, 2, 6)
    loc_rev = df.groupby("location")["purchase_amount"].sum().nlargest(10).sort_values()
    loc_rev.plot(kind="barh", ax=ax9, color="#bab0ab")
    ax9.set_title("Top 10 Locations by Revenue")
    ax9.set_xlabel("Revenue")

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(DASHBOARD_DIR / "customer_shopping_dashboard.png", dpi=180)
    plt.close(fig)


def create_html_dashboard(df: pd.DataFrame) -> None:
    total_revenue = df["purchase_amount"].sum()
    customers = df["customer_id"].nunique()
    aov = df["purchase_amount"].mean()
    subscriber_rate = (df["subscription_status"].eq("Yes").mean()) * 100
    churn_risk = int(df["churn_risk_flag"].sum())

    tables = {
        "Revenue by Gender": df.groupby("gender")["purchase_amount"].sum().reset_index(),
        "Revenue by Category": df.groupby("category")["purchase_amount"].sum().sort_values(ascending=False).reset_index(),
        "Revenue by Season": df.groupby("season")["purchase_amount"].sum().sort_values(ascending=False).reset_index(),
        "Discount Impact": df.groupby("discount_applied").agg(
            customers=("customer_id", "count"),
            revenue=("purchase_amount", "sum"),
            avg_order_value=("purchase_amount", "mean"),
        ).round(2).reset_index(),
        "Top 10 Locations": df.groupby("location")["purchase_amount"].sum().nlargest(10).reset_index(),
    }

    cards = f"""
    <div class="cards">
      <div class="card"><span>Total Revenue</span><strong>${total_revenue:,.0f}</strong></div>
      <div class="card"><span>Customers</span><strong>{customers:,.0f}</strong></div>
      <div class="card"><span>Average Order Value</span><strong>${aov:,.2f}</strong></div>
      <div class="card"><span>Subscriber Rate</span><strong>{subscriber_rate:.1f}%</strong></div>
      <div class="card"><span>Churn-Risk Customers</span><strong>{churn_risk}</strong></div>
    </div>
    """
    table_html = "\n".join(
        f"<section><h2>{title}</h2>{table.to_html(index=False, classes='data-table')}</section>"
        for title, table in tables.items()
    )
    html = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Customer Shopping Dashboard</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2933; background: #f7f9fb; }}
        h1 {{ margin-bottom: 8px; }}
        .subtitle {{ color: #52606d; margin-bottom: 24px; }}
        .cards {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 24px; }}
        .card {{ background: white; border: 1px solid #d9e2ec; padding: 18px; border-radius: 8px; }}
        .card span {{ display: block; color: #52606d; font-size: 13px; }}
        .card strong {{ display: block; font-size: 24px; margin-top: 8px; }}
        img {{ max-width: 100%; border: 1px solid #d9e2ec; border-radius: 8px; background: white; }}
        section {{ background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 18px; margin-top: 18px; }}
        .data-table {{ border-collapse: collapse; width: 100%; }}
        .data-table th, .data-table td {{ border-bottom: 1px solid #e5e7eb; padding: 8px; text-align: left; }}
      </style>
    </head>
    <body>
      <h1>Customer Shopping Behavior Dashboard</h1>
      <p class="subtitle">Revenue, segmentation, discount impact, and retention overview.</p>
      {cards}
      <img src="customer_shopping_dashboard.png" alt="Customer shopping dashboard">
      {table_html}
    </body>
    </html>
    """
    (DASHBOARD_DIR / "customer_shopping_dashboard.html").write_text(html, encoding="utf-8")


def main() -> None:
    df = clean_data()
    create_png_dashboard(df)
    create_html_dashboard(df)
    print("Created customer dashboard PNG and HTML.")


if __name__ == "__main__":
    main()
