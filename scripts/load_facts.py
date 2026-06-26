import pandas as pd
from sqlalchemy import create_engine

# Connect to SQLite
engine = create_engine("sqlite:///bluestock_mf.db")

# ==========================
# Load FACT_NAV
# ==========================

nav = pd.read_csv("data/processed/02_nav_history_clean.csv")
nav["date"] = pd.to_datetime(nav["date"])

dim_date = pd.read_sql("SELECT * FROM dim_date", engine)
dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])

nav = nav.merge(
    dim_date[["date_id", "full_date"]],
    left_on="date",
    right_on="full_date",
    how="left"
)

fact_nav = nav[
    [
        "amfi_code",
        "date_id",
        "nav"
    ]
]

fact_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)

print("fact_nav loaded successfully!")

# ==========================
# Load FACT_TRANSACTIONS
# ==========================

transactions = pd.read_csv(
    "data/processed/08_investor_transactions_clean.csv"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

transactions = transactions.merge(
    dim_date[["date_id", "full_date"]],
    left_on="transaction_date",
    right_on="full_date",
    how="left"
)

fact_transactions = transactions[
    [
        "investor_id",
        "amfi_code",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "date_id",
        "transaction_type",
        "gender",
        "annual_income_lakh",
        "payment_mode",
        "kyc_status"
    ]
]

fact_transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

print("fact_transactions loaded successfully!")

# ==========================
# Load FACT_PERFORMANCE
# ==========================

performance = pd.read_csv(
    "data/processed/07_scheme_performance_clean.csv"
)

fact_performance = performance[
    [
        "amfi_code",
        "fund_house",
        "category",
        "plan",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "expense_ratio_pct"
    ]
]

fact_performance.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

print("fact_performance loaded successfully!")

# ==========================
# Load FACT_AUM
# ==========================

fact_aum = performance[
    [
        "amfi_code",
        "aum_crore"
    ]
]

fact_aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)

print("fact_aum loaded successfully!")

print("\nAll fact tables loaded successfully!")