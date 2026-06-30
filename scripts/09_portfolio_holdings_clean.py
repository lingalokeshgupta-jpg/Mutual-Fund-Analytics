import pandas as pd

# Load dataset
portfolio = pd.read_csv("data/raw/09_portfolio_holdings.csv")

# Standardize column names
portfolio.columns = (
    portfolio.columns.str.strip()
                     .str.lower()
                     .str.replace(" ", "_")
)

# Remove duplicate rows
portfolio = portfolio.drop_duplicates()

# Remove extra spaces
for col in portfolio.select_dtypes(include="object"):
    portfolio[col] = portfolio[col].str.strip()

# Convert portfolio date
portfolio["portfolio_date"] = pd.to_datetime(
    portfolio["portfolio_date"],
    errors="coerce"
)

# Convert numeric columns
numeric_cols = [
    "weight_pct",
    "market_value_cr",
    "current_price_inr"
]

for col in numeric_cols:
    portfolio[col] = pd.to_numeric(portfolio[col], errors="coerce")

# Check missing values
print(portfolio.isnull().sum())

# Save cleaned dataset
portfolio.to_csv("data/processed/09_portfolio_holdings_clean.csv", index=False)

print("09_portfolio_holdings cleaned successfully!")

print(portfolio.info())
print(portfolio.head())