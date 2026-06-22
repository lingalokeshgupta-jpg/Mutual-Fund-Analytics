import requests
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url)

data = response.json()

print(data)

nav_df = pd.DataFrame(data["data"])

nav_df.to_csv(
    "data/raw/hdfc_top100_nav.csv",
    index = False
)

scheme_codes = [ 
    119551,
    120503,
    118632,
    119092,
    120841
]

for code in scheme_codes:

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    data = response.json()

    data = pd.DataFrame(data["data"])

    nav_df.to_csv(
        f"data/raw/{code}.csv",
        index = False

    )

    print(f"{code} downloaded")

df = pd.read_csv("data/raw/fund_master.csv")

print(df['fund_house'].unique())

print(df['category'].unique())

print(df['sub_category'].unique())

print(df['risk_grade'].unique())

fund_master = pd.read_csv("data/raw/fund_master.csv")
nav_history = pd.read_csv("data/raw/nav_history.csv")

missing_codes = set(fund_master['amfi_code']) - set(nav_history['amfi_code'])

print(missing_codes)