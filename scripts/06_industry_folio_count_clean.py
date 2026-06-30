import pandas as pd

# Load dataset
folio = pd.read_csv("data/raw/06_industry_folio_count.csv")

# Standardize column names
folio.columns = (
    folio.columns.str.strip()
                 .str.lower()
                 .str.replace(" ", "_")
)

# Remove duplicate rows
folio = folio.drop_duplicates()

# Remove extra spaces from text columns
for col in folio.select_dtypes(include="object"):
    folio[col] = folio[col].str.strip()

# Convert month to datetime
folio["month"] = pd.to_datetime(folio["month"], format="%Y-%m", errors="coerce")

# Convert numeric columns
numeric_cols = [
    "total_folios_crore",
    "equity_folios_crore",
    "debt_folios_crore",
    "hybrid_folios_crore",
    "others_folios_crore"
]

for col in numeric_cols:
    folio[col] = pd.to_numeric(folio[col], errors="coerce")

# Check missing values
print(folio.isnull().sum())

# Save cleaned dataset
folio.to_csv("data/processed/06_industry_folio_count_clean.csv", index=False)

print("06_industry_folio_count cleaned successfully!")

