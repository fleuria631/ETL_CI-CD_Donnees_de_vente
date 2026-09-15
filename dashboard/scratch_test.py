from db import run_query

min_max = run_query("SELECT MIN(full_date) as min_date, MAX(full_date) as max_date FROM analytics_marts.fact_sales fs JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key")
print(min_max)
