import pandas as pd
pref = pd.read_csv("data/raw/07_scheme_performance.csv")
pref['return_1yr_pct'] = pd.to_numeric(pref['return_1yr_pct'], errors='coerce')
pref['return_3yr_pct'] = pd.to_numeric(pref['return_3yr_pct'], errors='coerce')
pref['return_5yr_pct'] = pd.to_numeric(pref['return_5yr_pct'], errors='coerce')
pref = pref[(pref['expense_ratio_pct'] >= 0.1) & (pref['expense_ratio_pct'] <= 2.5)]
anomalies = pref[(pref['return_1yr_pct'] > 100) | (pref['return_3yr_pct'] < -100)]
pref.to_csv("data/processed/07_scheme_performance_clean.csv", index=False) 
print(pref.columns)
print(pref.head())
                