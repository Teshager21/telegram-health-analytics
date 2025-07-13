{{ config(materialized='table') }}

SELECT DISTINCT
    date::date AS date_id,
    EXTRACT(year FROM date) AS year,
    EXTRACT(month FROM date) AS month,
    EXTRACT(day FROM date) AS day
FROM
    {{ ref('stg_telegram_messages') }}
WHERE
    date IS NOT NULL
