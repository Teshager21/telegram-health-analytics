{{ config(
    materialized='table'
) }}

SELECT
    lower(product_name) as product_name,
    COUNT(*) AS mentions
FROM
    {{ ref('stg_telegram_messages') }}
WHERE
    product_name IS NOT NULL
GROUP BY
    lower(product_name)
ORDER BY
    mentions DESC
