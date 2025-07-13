{{ config(materialized='table') }}

select
    message_id,
    message_date,
    channel_name,
    has_media,
    media_file,
    length(message) as message_length,
    load_date
from {{ ref('stg_telegram_messages') }}
