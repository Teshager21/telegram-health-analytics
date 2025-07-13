{{ config(materialized='table') }}

SELECT DISTINCT
    channel_name AS channel_id,
    channel_name AS channel_name
FROM
    {{ ref('stg_telegram_messages') }}
