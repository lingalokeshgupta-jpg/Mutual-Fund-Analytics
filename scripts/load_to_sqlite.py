import sqlite3
import pandas as pd

# -----------------------------
# Connect to SQLite
# -----------------------------
conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()

# -----------------------------
# Read all cleaned CSVs
# -----------------------------
fund = pd.read_csv("data/processed/01_fund_master_clean.csv")
nav = pd.read_csv("data/processed/02_nav_history_clean.csv")
aum = pd.read_csv("data/processed/03_aum_by_fund_house_clean.csv")
sip = pd.read_csv("data/processed/04_monthly_sip_inflows_clean.csv")
category = pd.read_csv("data/processed/05_category_inflows_clean.csv")
folio = pd.read_csv("data/processed/06_industry_folio_count_clean.csv")
performance = pd.read_csv("data/processed/07_scheme_performance_clean.csv")
transactions = pd.read_csv("data/processed/08_investor_transactions_clean.csv")
portfolio = pd.read_csv("data/processed/09_portfolio_holdings_clean.csv")
benchmark = pd.read_csv("data/processed/10_benchmark_indices_clean.csv")

# -----------------------------
# Convert date columns
# -----------------------------
fund["launch_date"] = pd.to_datetime(
    fund["launch_date"],
    dayfirst=True,
    errors="coerce"
)

nav["date"] = pd.to_datetime(
    nav["date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

aum["date"] = pd.to_datetime(
    aum["date"],
    dayfirst=True
)

sip["month"] = pd.to_datetime(
    sip["month"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

category["month"] = pd.to_datetime(
    category["month"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

folio["month"] = pd.to_datetime(
    folio["month"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

portfolio["portfolio_date"] = pd.to_datetime(
    portfolio["portfolio_date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

benchmark["date"] = pd.to_datetime(
    benchmark["date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# -----------------------------
# Load dim_fund
# -----------------------------
fund.to_sql(
    "dim_fund",
    conn,
    if_exists="append",
    index=False
)

print("✓ dim_fund loaded")

# -----------------------------
# Create dim_date
# -----------------------------
all_dates = pd.concat([
    nav["date"],
    aum["date"],
    sip["month"],
    category["month"],
    folio["month"],
    transactions["transaction_date"],
    portfolio["portfolio_date"],
    benchmark["date"]
]).drop_duplicates().sort_values()

dim_date = pd.DataFrame({
    "full_date": all_dates
})

dim_date["year"] = dim_date["full_date"].dt.year
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["quarter"] = dim_date["full_date"].dt.quarter

dim_date.to_sql(
    "dim_date",
    conn,
    if_exists="append",
    index=False
)

print("✓ dim_date loaded")

# -----------------------------
# Create date lookup dictionary
# -----------------------------
date_lookup = pd.read_sql(
    "SELECT date_id, full_date FROM dim_date",
    conn
)

date_lookup["full_date"] = pd.to_datetime(date_lookup["full_date"])

date_dict = dict(
    zip(
        date_lookup["full_date"],
        date_lookup["date_id"]
    )
)

print("✓ Date lookup created")

# -----------------------------
# Load fact_nav
# -----------------------------
nav["date_id"] = nav["date"].map(date_dict)

nav[["amfi_code", "date_id", "nav"]].to_sql(
    "fact_nav",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_nav loaded")

# -----------------------------
# Load fact_transactions
# -----------------------------
transactions["date_id"] = transactions["transaction_date"].map(date_dict)

transactions[
    [
        "investor_id",
        "amfi_code",
        "amount_inr",
        "state",
        "city",
        "city_tier",
        "age_group",
        "gender",
        "annual_income_lakh",
        "transaction_type",
        "payment_mode",
        "kyc_status",
        "date_id",
    ]
].to_sql(
    "fact_transactions",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_transactions loaded")

# -----------------------------
# Load fact_performance
# -----------------------------
performance[
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
        "expense_ratio_pct",
    ]
].to_sql(
    "fact_performance",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_performance loaded")

# -----------------------------
# Load fact_aum
# -----------------------------
aum["date_id"] = aum["date"].map(date_dict)

aum[
    [
        "date_id",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes",
    ]
].to_sql(
    "fact_aum",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_aum loaded")

# -----------------------------
# Load fact_sip_inflows
# -----------------------------
sip["date_id"] = sip["month"].map(date_dict)

sip[
    [
        "date_id",
        "sip_inflow_crore",
        "active_sip_accounts_crore",
        "new_sip_accounts_lakh",
        "sip_aum_lakh_crore",
        "yoy_growth_pct",
    ]
].to_sql(
    "fact_sip_inflows",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_sip_inflows loaded")

# -----------------------------
# Load fact_category_inflows
# -----------------------------
category["date_id"] = category["month"].map(date_dict)

category[
    [
        "date_id",
        "category",
        "net_inflow_crore",
    ]
].to_sql(
    "fact_category_inflows",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_category_inflows loaded")

# -----------------------------
# Load fact_folio_count
# -----------------------------
folio["date_id"] = folio["month"].map(date_dict)

folio[
    [
        "date_id",
        "total_folios_crore",
        "equity_folios_crore",
        "debt_folios_crore",
        "hybrid_folios_crore",
        "others_folios_crore",
    ]
].to_sql(
    "fact_folio_count",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_folio_count loaded")

# -----------------------------
# Load fact_portfolio_holdings
# -----------------------------
portfolio["date_id"] = portfolio["portfolio_date"].map(date_dict)

portfolio[
    [
        "amfi_code",
        "stock_symbol",
        "stock_name",
        "sector",
        "weight_pct",
        "market_value_cr",
        "current_price_inr",
        "date_id",
    ]
].to_sql(
    "fact_portfolio_holdings",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_portfolio_holdings loaded")

# -----------------------------
# Load fact_benchmark_indices
# -----------------------------
benchmark["date_id"] = benchmark["date"].map(date_dict)

benchmark[
    [
        "date_id",
        "index_name",
        "close_value",
    ]
].to_sql(
    "fact_benchmark_indices",
    conn,
    if_exists="append",
    index=False
)

print("✓ fact_benchmark_indices loaded")


# -----------------------------
# Commit changes
# -----------------------------
conn.commit()

print("\n==============================")
print("DATABASE LOAD COMPLETE")
print("==============================")

# -----------------------------
# Print row counts
# -----------------------------
tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
    "fact_sip_inflows",
    "fact_category_inflows",
    "fact_folio_count",
    "fact_portfolio_holdings",
    "fact_benchmark_indices"
]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:<30} : {count:,} rows")

# -----------------------------
# Close database
# -----------------------------
conn.close()

print("\n✓ SQLite connection closed.")
print("✓ All tables loaded successfully.")