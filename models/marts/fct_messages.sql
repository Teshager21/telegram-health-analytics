{{ config(materialized='table') }}

SELECT
    id AS message_id,
    date::date AS date_id,
    channel_name AS channel_id,
    sender_id,
    has_media,
    message_length,
    media_file
FROM
    {{ ref('stg_telegram_messages') }}
