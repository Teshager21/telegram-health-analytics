{{ config(
    materialized='view'
) }}

with raw_messages as (
    select
        id,
        date,
        message,
        sender_id,
        has_media,
        media_file,
        channel_name,
        load_date
    from raw.telegram_messages
)

select
    id as message_id,
    date as message_date,
    message,
    sender_id,
    has_media,
    media_file,
    channel_name,
    load_date
from raw_messages
