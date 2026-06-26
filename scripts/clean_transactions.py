import pandas as pd
tx = pd.read_csv("data/raw/08_investor_transactions.csv")
tx['transaction_type'] = (tx['transaction_type'].str.strip().str.title())
valid_types = ['Sip', 'Redemption', 'Lumpsum']
tx = tx[tx['transaction_type'].isin(valid_types)]
tx = tx[tx['amount_inr'] > 0]
tx['transaction_date'] = pd.to_datetime(tx['transaction_date'])
valid_kyc = ['Verified', 'Pending', 'Rejected']
tx = tx[tx['kyc_status'].isin(valid_kyc)]
tx.to_csv("data/processed/08_investor_transactions_clean.csv", index=False)
print(tx.columns)
print(tx.head())