# Data Dictionary – Mutual Fund Analytics

## Overview

This document describes the SQLite database schema used in the Mutual Fund Analytics Capstone Project. It includes table descriptions, column names, data types, business definitions, and source datasets.

---

# Table: dim_fund

**Description:** Stores master information about each mutual fund scheme.

| Column               | Data Type | Business Definition                         | Source                          |
| -------------------- | --------- | ------------------------------------------- | ------------------------------- |
| amfi_code            | INTEGER   | Unique identifier of the mutual fund scheme | 07_scheme_performance_clean.csv |
| scheme_name          | TEXT      | Name of the mutual fund scheme              | 07_scheme_performance_clean.csv |
| fund_house           | TEXT      | Asset Management Company (AMC)              | 07_scheme_performance_clean.csv |
| category             | TEXT      | Fund category (Large Cap, Mid Cap, etc.)    | 07_scheme_performance_clean.csv |
| plan                 | TEXT      | Investment plan (Regular/Direct)            | 07_scheme_performance_clean.csv |
| morningstar_category | INTEGER   | Morningstar rating/category                 | 07_scheme_performance_clean.csv |
| risk_grade           | TEXT      | Risk level of the fund                      | 07_scheme_performance_clean.csv |

---

# Table: dim_date

**Description:** Date dimension used for time-based analysis.

| Column    | Data Type | Business Definition    | Source             |
| --------- | --------- | ---------------------- | ------------------ |
| date_id   | INTEGER   | Surrogate key for date | Generated          |
| full_date | DATE      | Calendar date          | NAV & Transactions |
| year      | INTEGER   | Year                   | Generated          |
| month     | INTEGER   | Month number           | Generated          |
| quarter   | INTEGER   | Quarter (1–4)          | Generated          |

---

# Table: fact_nav

**Description:** Stores daily NAV values.

| Column    | Data Type | Business Definition    | Source                   |
| --------- | --------- | ---------------------- | ------------------------ |
| nav_id    | INTEGER   | Primary key            | Generated                |
| amfi_code | INTEGER   | Mutual fund identifier | 02_nav_history_clean.csv |
| date_id   | INTEGER   | Date reference         | dim_date                 |
| nav       | REAL      | Net Asset Value        | 02_nav_history_clean.csv |

---

# Table: fact_transactions

**Description:** Stores investor transaction details.

| Column             | Data Type | Business Definition        | Source                             |
| ------------------ | --------- | -------------------------- | ---------------------------------- |
| transaction_id     | INTEGER   | Primary key                | Generated                          |
| investor_id        | INTEGER   | Investor identifier        | 08_investor_transactions_clean.csv |
| amfi_code          | INTEGER   | Mutual fund identifier     | 08_investor_transactions_clean.csv |
| amount_inr         | REAL      | Transaction amount (₹)     | 08_investor_transactions_clean.csv |
| state              | TEXT      | Investor state             | 08_investor_transactions_clean.csv |
| city               | TEXT      | Investor city              | 08_investor_transactions_clean.csv |
| city_tier          | TEXT      | Tier of city               | 08_investor_transactions_clean.csv |
| age_group          | TEXT      | Investor age category      | 08_investor_transactions_clean.csv |
| date_id            | INTEGER   | Date reference             | dim_date                           |
| transaction_type   | TEXT      | SIP, Lumpsum or Redemption | 08_investor_transactions_clean.csv |
| gender             | TEXT      | Investor gender            | 08_investor_transactions_clean.csv |
| annual_income_lakh | REAL      | Annual income (lakhs)      | 08_investor_transactions_clean.csv |
| payment_mode       | TEXT      | Payment method             | 08_investor_transactions_clean.csv |
| kyc_status         | TEXT      | KYC verification status    | 08_investor_transactions_clean.csv |

---

# Table: fact_performance

**Description:** Stores mutual fund performance metrics.

| Column            | Data Type | Business Definition           | Source                          |
| ----------------- | --------- | ----------------------------- | ------------------------------- |
| performance_id    | INTEGER   | Primary key                   | Generated                       |
| amfi_code         | INTEGER   | Mutual fund identifier        | 07_scheme_performance_clean.csv |
| fund_house        | TEXT      | AMC name                      | 07_scheme_performance_clean.csv |
| category          | TEXT      | Fund category                 | 07_scheme_performance_clean.csv |
| plan              | TEXT      | Investment plan               | 07_scheme_performance_clean.csv |
| return_1yr_pct    | REAL      | One-year return (%)           | 07_scheme_performance_clean.csv |
| return_3yr_pct    | REAL      | Three-year return (%)         | 07_scheme_performance_clean.csv |
| return_5yr_pct    | REAL      | Five-year return (%)          | 07_scheme_performance_clean.csv |
| benchmark_3yr_pct | REAL      | Benchmark return (%)          | 07_scheme_performance_clean.csv |
| alpha             | REAL      | Alpha metric                  | 07_scheme_performance_clean.csv |
| beta              | REAL      | Beta metric                   | 07_scheme_performance_clean.csv |
| sharpe_ratio      | REAL      | Sharpe Ratio                  | 07_scheme_performance_clean.csv |
| sortino_ratio     | REAL      | Sortino Ratio                 | 07_scheme_performance_clean.csv |
| std_dev_ann_pct   | REAL      | Annualized Standard Deviation | 07_scheme_performance_clean.csv |
| max_drawdown_pct  | REAL      | Maximum Drawdown (%)          | 07_scheme_performance_clean.csv |
| expense_ratio_pct | REAL      | Expense Ratio (%)             | 07_scheme_performance_clean.csv |

---

# Table: fact_aum

**Description:** Stores Assets Under Management (AUM).

| Column    | Data Type | Business Definition                | Source                          |
| --------- | --------- | ---------------------------------- | ------------------------------- |
| aum_id    | INTEGER   | Primary key                        | Generated                       |
| amfi_code | INTEGER   | Mutual fund identifier             | 07_scheme_performance_clean.csv |
| aum_crore | REAL      | Assets Under Management (₹ Crores) | 07_scheme_performance_clean.csv |
