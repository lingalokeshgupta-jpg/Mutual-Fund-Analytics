import pandas as pd

# Load dataset
fund = pd.read_csv("data/raw/01_fund_master.csv")

# Standardize column names
fund.columns = (
    fund.columns.str.strip()
                .str.lower()
                .str.replace(" ", "_")
)

# Remove duplicate rows
fund = fund.drop_duplicates()

# Remove extra spaces from text columns
for col in fund.select_dtypes(include="object"):
    fund[col] = fund[col].str.strip()

# Convert launch_date to datetime
fund["launch_date"] = pd.to_datetime(fund["launch_date"], errors="coerce")

# Check missing values
print(fund.isnull().sum())

# Save cleaned dataset
fund.to_csv("data/processed/01_fund_master_clean.csv", index=False)

print("01_fund_master cleaned successfully!")

