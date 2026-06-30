CREATE TABLE dim_fund(
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount INTEGER,
    min_lumpsum_amount INTEGER,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

CREATE TABLE dim_date(
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE UNIQUE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER
);

CREATE TABLE fact_nav(
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_id INTEGER,
    nav REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_transactions(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id INTEGER,
    amfi_code INTEGER,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    transaction_type TEXT,
    payment_mode TEXT,
    kyc_status TEXT,
    date_id INTEGER,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_performance(

    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    fund_house TEXT,
    category TEXT,
    plan TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    expense_ratio_pct REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);

create table fact_aum(
    aum_id integer primary key autoincrement,
    amfi_code integer,      
    aum_crore real,
    foreign key(amfi_code) references dim_fund(amfi_code)
);

-- ===========================================
-- FACT: Monthly SIP Inflows
-- ===========================================

CREATE TABLE fact_sip_inflows(
    sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL,
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);


-- ===========================================
-- FACT: Category-wise Inflows
-- ===========================================

CREATE TABLE fact_category_inflows(
    category_inflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    category TEXT,
    net_inflow_crore REAL,
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);


-- ===========================================
-- FACT: Industry Folio Count
-- ===========================================

CREATE TABLE fact_folio_count(
    folio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL,
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);


-- ===========================================
-- FACT: Portfolio Holdings
-- ===========================================

CREATE TABLE fact_portfolio_holdings(
    holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    stock_symbol TEXT,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    date_id INTEGER,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);


-- ===========================================
-- FACT: Benchmark Indices
-- ===========================================

CREATE TABLE fact_benchmark_indices(
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    index_name TEXT,
    close_value REAL,
    FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);