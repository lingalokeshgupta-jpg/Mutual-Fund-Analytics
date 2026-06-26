import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('sqlite:///bluestock_mf.db')
print("database connected successfully")

nav = pd.read_csv("data/processed/02_nav_history_clean.csv ")
transactions = pd.read_csv("data/processed/08_investor_transactions_clean.csv")
performance = pd.read_csv("data/processed/07_scheme_performance_clean.csv")

nav.to_sql("fact_nav", engine, if_exists="append", index=False)

transactions.to_sql("fact_transactions", engine, if_exists="append", index=False)

performance.to_sql("fact_performance", engine, if_exists="append", index=False)

print("All cleaned data loaded successfully")