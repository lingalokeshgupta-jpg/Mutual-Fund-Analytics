import pandas as pd

# Load dataset
category = pd.read_csv("data/raw/05_category_inflows.csv")

# Standardize column names
category.columns = category.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicates
category = category.drop_duplicates()

# Remove extra spaces
for col in category.select_dtypes(include="object"):
    category[col] = category[col].str.strip()

# Convert month to datetime
category["month"] = pd.to_datetime(category["month"], format="%Y-%m", errors="coerce")

# Convert numeric column
category["net_inflow_crore"] = pd.to_numeric(
    category["net_inflow_crore"],
    errors="coerce"
)

print(category.isnull().sum())

category.to_csv("data/processed/05_category_inflows_clean.csv", index=False)

print("05_category_inflows cleaned successfully!")
print(category.info())  
print(category.head())