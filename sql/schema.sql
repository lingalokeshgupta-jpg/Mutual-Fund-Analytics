create table dim_fund(
    amfi_code integer primary key,
    scheme_name text,
    fund_house text,
    category text,
    plan text,
    morningstar_category integer,
    risk_grade text
);

create table dim_date(
    date_id integer primary key autoincrement,
    full_date date unique,
    year integer,
    month integer,  
    quarter integer
);

create table fact_nav(
    nav_id integer primary key autoincrement,
    amfi_code integer,
    date_id integer,
    nav real,   
    foreign key(amfi_code) references dim_fund(amfi_code),
    foreign key(date_id) references dim_date(date_id)
);

create table fact_transactions(
    investor_id integer,
    transaction_id integer primary key autoincrement,
    amfi_code integer,
    amount_inr real,
    state text,
    city text,
    city_tier text,
    age_group text,
    date_id integer,
    transaction_type text,
    gender text,
    annual_income_lakh real,
    payment_mode text,
    kyc_status text,
    foreign key(amfi_code) references dim_fund(amfi_code),
    foreign key(date_id) references dim_date(date_id)
);

create table fact_performance(
    performance_id integer primary key autoincrement,
    amfi_code integer,
    fund_house text,
    category text,
    plan text,
    return_1yr_pct real,
    return_3yr_pct real,
    return_5yr_pct real,
    benchmark_3yr_pct real,
    alpha real,
    beta real,
    sharpe_ratio real,
    sortino_ratio real,
    std_dev_ann_pct real,
    max_drawdown_pct real,
    expense_ratio_pct real,
    foreign key(amfi_code) references dim_fund(amfi_code)
);

create table fact_aum(
    aum_id integer primary key autoincrement,
    amfi_code integer,      
    aum_crore real,
    foreign key(amfi_code) references dim_fund(amfi_code)
);