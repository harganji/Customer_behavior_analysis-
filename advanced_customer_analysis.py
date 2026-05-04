from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    mean_absolute_error,
    r2_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "customer_shopping_behavior.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


FREQUENCY_TO_DAYS = {
    "Weekly": 7,
    "Fortnightly": 14,
    "Bi-Weekly": 14,
    "Monthly": 30,
    "Quarterly": 90,
    "Every 3 Months": 90,
    "Annually": 365,
}


def load_and_clean_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

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
    if "promo_code_used" in df.columns:
        df = df.drop(columns=["promo_code_used"])

    labels = ["Young Adult", "Adult", "Middle-aged", "Senior"]
    df["age_group"] = pd.qcut(df["age"], q=4, labels=labels)
    df["purchase_frequency_days"] = df["frequency_of_purchases"].map(FREQUENCY_TO_DAYS)
    df["estimated_annual_orders"] = (365 / df["purchase_frequency_days"]).round(2)
    df["estimated_customer_lifetime_value"] = (
        df["purchase_amount"] * (df["previous_purchases"] + df["estimated_annual_orders"])
    ).round(2)

    df["is_subscriber"] = (df["subscription_status"] == "Yes").astype(int)
    df["used_discount"] = (df["discount_applied"] == "Yes").astype(int)
    df["high_value_customer"] = (
        df["estimated_customer_lifetime_value"]
        >= df["estimated_customer_lifetime_value"].quantile(0.75)
    ).astype(int)

    df["purchase_recency_score"] = pd.qcut(
        df["purchase_frequency_days"].rank(method="first", ascending=False),
        4,
        labels=[1, 2, 3, 4],
    ).astype(int)
    df["frequency_score"] = pd.qcut(
        df["previous_purchases"].rank(method="first"), 4, labels=[1, 2, 3, 4]
    ).astype(int)
    df["monetary_score"] = pd.qcut(
        df["purchase_amount"].rank(method="first"), 4, labels=[1, 2, 3, 4]
    ).astype(int)
    df["rfm_score"] = (
        df["purchase_recency_score"] + df["frequency_score"] + df["monetary_score"]
    )

    conditions = [
        df["rfm_score"] >= 10,
        df["rfm_score"].between(8, 9),
        df["rfm_score"].between(6, 7),
        df["rfm_score"] <= 5,
    ]
    labels = ["Champions", "Loyal Growth", "At Risk", "Low Engagement"]
    df["rfm_segment"] = np.select(conditions, labels, default="Monitor")

    df["churn_risk_flag"] = np.where(
        (df["subscription_status"] == "No")
        & (df["purchase_frequency_days"] >= 90)
        & (df["previous_purchases"] <= df["previous_purchases"].median()),
        1,
        0,
    )

    return df


def build_business_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    gender_revenue = (
        df.groupby("gender")
        .agg(
            customers=("customer_id", "count"),
            revenue=("purchase_amount", "sum"),
            avg_order_value=("purchase_amount", "mean"),
            avg_estimated_clv=("estimated_customer_lifetime_value", "mean"),
        )
        .round(2)
        .sort_values("revenue", ascending=False)
    )

    segment_summary = (
        df.groupby("rfm_segment")
        .agg(
            customers=("customer_id", "count"),
            revenue=("purchase_amount", "sum"),
            avg_order_value=("purchase_amount", "mean"),
            avg_estimated_clv=("estimated_customer_lifetime_value", "mean"),
            churn_risk_rate=("churn_risk_flag", "mean"),
        )
        .round(3)
        .sort_values("avg_estimated_clv", ascending=False)
    )

    discount_impact = (
        df.groupby("discount_applied")
        .agg(
            customers=("customer_id", "count"),
            revenue=("purchase_amount", "sum"),
            avg_order_value=("purchase_amount", "mean"),
            avg_previous_purchases=("previous_purchases", "mean"),
            avg_estimated_clv=("estimated_customer_lifetime_value", "mean"),
        )
        .round(2)
    )

    category_insights = (
        df.groupby("category")
        .agg(
            revenue=("purchase_amount", "sum"),
            customers=("customer_id", "count"),
            avg_review_rating=("review_rating", "mean"),
            avg_estimated_clv=("estimated_customer_lifetime_value", "mean"),
        )
        .round(2)
        .sort_values("revenue", ascending=False)
    )

    correlation = (
        df[
            [
                "age",
                "purchase_amount",
                "review_rating",
                "previous_purchases",
                "purchase_frequency_days",
                "estimated_annual_orders",
                "estimated_customer_lifetime_value",
                "is_subscriber",
                "used_discount",
                "churn_risk_flag",
            ]
        ]
        .corr(numeric_only=True)
        .round(3)
    )

    return {
        "gender_revenue": gender_revenue,
        "rfm_segment_summary": segment_summary,
        "discount_impact": discount_impact,
        "category_insights": category_insights,
        "correlation_matrix": correlation,
    }


def train_models(df: pd.DataFrame) -> dict[str, object]:
    features = [
        "age",
        "gender",
        "category",
        "location",
        "season",
        "review_rating",
        "subscription_status",
        "shipping_type",
        "discount_applied",
        "previous_purchases",
        "payment_method",
        "frequency_of_purchases",
        "age_group",
    ]

    X = df[features]
    numeric_features = ["age", "review_rating", "previous_purchases"]
    categorical_features = [col for col in features if col not in numeric_features]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                numeric_features,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        df["high_value_customer"],
        test_size=0.25,
        random_state=42,
        stratify=df["high_value_customer"],
    )

    classifier = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=42,
                    class_weight="balanced",
                    min_samples_leaf=4,
                ),
            ),
        ]
    )
    classifier.fit(X_train, y_train)
    class_pred = classifier.predict(X_test)
    class_prob = classifier.predict_proba(X_test)[:, 1]

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X, df["purchase_amount"], test_size=0.25, random_state=42
    )
    regressor = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=300,
                    random_state=42,
                    min_samples_leaf=4,
                ),
            ),
        ]
    )
    regressor.fit(X_train_r, y_train_r)
    reg_pred = regressor.predict(X_test_r)

    return {
        "classification_accuracy": round(accuracy_score(y_test, class_pred), 3),
        "classification_roc_auc": round(roc_auc_score(y_test, class_prob), 3),
        "classification_report": classification_report(y_test, class_pred),
        "regression_mae": round(mean_absolute_error(y_test_r, reg_pred), 2),
        "regression_r2": round(r2_score(y_test_r, reg_pred), 3),
    }


def write_outputs(tables: dict[str, pd.DataFrame], model_results: dict[str, object]) -> None:
    for name, table in tables.items():
        table.to_csv(OUTPUT_DIR / f"{name}.csv")

    summary_lines = [
        "Customer Shopping Behavior Analysis - Model Results",
        "",
        f"High-value customer classifier accuracy: {model_results['classification_accuracy']}",
        f"High-value customer classifier ROC AUC: {model_results['classification_roc_auc']}",
        f"Purchase amount regression MAE: ${model_results['regression_mae']}",
        f"Purchase amount regression R2: {model_results['regression_r2']}",
        "",
        "Classification report:",
        str(model_results["classification_report"]),
    ]
    (OUTPUT_DIR / "model_results.txt").write_text("\n".join(summary_lines), encoding="utf-8")


def main() -> None:
    df = load_and_clean_data()
    tables = build_business_tables(df)
    model_results = train_models(df)
    write_outputs(tables, model_results)

    print("Rows analyzed:", len(df))
    print("Total revenue:", f"${df['purchase_amount'].sum():,.0f}")
    print("\nRevenue by gender")
    print(tables["gender_revenue"])
    print("\nRFM segment summary")
    print(tables["rfm_segment_summary"])
    print("\nModel results")
    print("Classifier ROC AUC:", model_results["classification_roc_auc"])
    print("Regression MAE:", f"${model_results['regression_mae']}")


if __name__ == "__main__":
    main()
