import pandas as pd

# Load dataset
aum = pd.read_csv("data/raw/03_aum_by_fund_house.csv")

# Standardize column names
aum.columns = (
    aum.columns.str.strip()
               .str.lower()
               .str.replace(" ", "_")
)

# Remove duplicate rows
aum = aum.drop_duplicates()

# Remove extra spaces
for col in aum.select_dtypes(include="object"):
    aum[col] = aum[col].str.strip()

# Convert date column
aum["date"] = pd.to_datetime(aum["date"], errors="coerce")

# Ensure numeric columns
numeric_cols = [
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]

for col in numeric_cols:
    aum[col] = pd.to_numeric(aum[col], errors="coerce")

# Check missing values
print(aum.isnull().sum())

# Save cleaned dataset
aum.to_csv("data/processed/03_aum_by_fund_house_clean.csv", index=False)

print("03_aum_by_fund_house cleaned successfully!")

print(aum.info())
print(aum.head())