import pandas as pd

# Load dataset
sip = pd.read_csv("data/raw/04_monthly_sip_inflows.csv")

# Standardize column names
sip.columns = sip.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicates
sip = sip.drop_duplicates()

# Remove extra spaces
for col in sip.select_dtypes(include="object"):
    sip[col] = sip[col].str.strip()

# Convert month to datetime
sip["month"] = pd.to_datetime(sip["month"], format="%Y-%m", errors="coerce")

# Convert numeric columns
numeric_cols = [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore",
    "yoy_growth_pct"
]

for col in numeric_cols:
    sip[col] = pd.to_numeric(sip[col], errors="coerce")

print(sip.isnull().sum())

sip.to_csv("data/processed/04_monthly_sip_inflows_clean.csv", index=False)

print("04_monthly_sip_inflows cleaned successfully!")

