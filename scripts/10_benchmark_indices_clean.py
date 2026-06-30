import pandas as pd

# Load dataset
benchmark = pd.read_csv("data/raw/10_benchmark_indices.csv")

# Standardize column names
benchmark.columns = (
    benchmark.columns.str.strip()
                     .str.lower()
                     .str.replace(" ", "_")
)

# Remove duplicate rows
benchmark = benchmark.drop_duplicates()

# Remove extra spaces from text columns
for col in benchmark.select_dtypes(include="object"):
    benchmark[col] = benchmark[col].str.strip()

# Convert date column to datetime
benchmark["date"] = pd.to_datetime(
    benchmark["date"],
    errors="coerce"
)

# Convert close_value to numeric
benchmark["close_value"] = pd.to_numeric(
    benchmark["close_value"],
    errors="coerce"
)

# Check missing values
print(benchmark.isnull().sum())

# Save cleaned dataset
benchmark.to_csv(
    "data/processed/10_benchmark_indices_clean.csv",
    index=False
)

print("10_benchmark_indices cleaned successfully!")


print(benchmark.info())
print(benchmark.head())