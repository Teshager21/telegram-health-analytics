{{ config(materialized='table') }}

with dates as (
    select
        generate_series('2023-01-01'::date, '2025-12-31'::date, interval '1 day') as date
)

select
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    to_char(date, 'Day') as weekday
from dates
