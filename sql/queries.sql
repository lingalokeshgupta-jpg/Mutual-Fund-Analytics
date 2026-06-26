--Query 1: Top 5 Funds by AUM
SELECT
    d.scheme_name,
    f.aum_crore
FROM fact_aum f
JOIN dim_fund d
ON f.amfi_code = d.amfi_code
ORDER BY f.aum_crore DESC
LIMIT 5;


--Query 2: Average NAV Per Month
SELECT
    dd.year,
    dd.month,
    ROUND(AVG(fn.nav),2) AS average_nav
FROM fact_nav fn
JOIN dim_date dd
ON fn.date_id = dd.date_id
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;


--Query 3: SIP Amount by Year
SELECT
    dd.year,
    ROUND(SUM(ft.amount_inr),2) AS sip_amount
FROM fact_transactions ft
JOIN dim_date dd
ON ft.date_id = dd.date_id
WHERE LOWER(ft.transaction_type) = 'sip'
GROUP BY dd.year
ORDER BY dd.year;


--Query 4: Transactions by State
SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;


--Query 5: Funds with Expense Ratio Below 1%
SELECT
    d.scheme_name,
    p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund d
ON p.amfi_code = d.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;