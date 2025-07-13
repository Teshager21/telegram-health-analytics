{{ config(materialized='table') }}

select
    distinct channel_name
from {{ ref('stg_telegram_messages') }}
where channel_name is not null
