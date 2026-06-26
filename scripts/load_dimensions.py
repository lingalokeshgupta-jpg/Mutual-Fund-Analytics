import pandas as pd
from sqlalchemy import create_engine

# Connect to SQLite
engine = create_engine("sqlite:///bluestock_mf.db")

# -------------------------
# Load Scheme Performance
# -------------------------
scheme = pd.read_csv("data/processed/07_scheme_performance_clean.csv")

dim_fund = scheme[
    [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "plan",
        "morningstar_rating",
        "risk_grade",
    ]
].drop_duplicates()

dim_fund.rename(
    columns={"morningstar_rating": "morningstar_category"},
    inplace=True,
)

dim_fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False,
)

print("dim_fund loaded!")

# -------------------------
# Create Date Dimension
# -------------------------
nav = pd.read_csv("data/processed/02_nav_history_clean.csv")
txn = pd.read_csv("data/processed/08_investor_transactions_clean.csv")

dates = pd.concat(
    [
        pd.to_datetime(nav["date"]),
        pd.to_datetime(txn["transaction_date"]),
    ]
).drop_duplicates()

dim_date = pd.DataFrame()

dim_date["full_date"] = dates.sort_values().reset_index(drop=True)
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["quarter"] = dim_date["full_date"].dt.quarter

dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False,
)

print("dim_date loaded!")