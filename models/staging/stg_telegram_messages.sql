{{ config(materialized='view') }}

SELECT
    id,
    date,
    message,
    sender_id,
    has_media,
    media_file,
    channel_name,
    load_date,
    LENGTH(message) AS message_length
FROM
    raw.telegram_messages
