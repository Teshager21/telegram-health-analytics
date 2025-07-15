{{ config(
    materialized='view'
) }}

WITH raw_messages AS (
    SELECT
        id,
        date,
        message,
        sender_id,
        has_media,
        media_file,
        channel_name,
        load_date
    FROM raw.telegram_messages
)

SELECT
    id AS message_id,
    date AS message_date,
    message,
    sender_id,
    has_media,
    media_file,
    channel_name,
    load_date,

    -- NEW: Extract product name
    CASE
        WHEN lower(message) LIKE '%aptamil%' THEN 'APTAMIL'
        WHEN lower(message) LIKE '%biotin%' THEN 'BIOTIN'
        WHEN lower(message) LIKE '%olive oil%' THEN 'ORGANIC EXTRA OLIVE OIL'
        -- add more conditions as needed, e.g.:
        -- WHEN lower(message) LIKE '%vitamin c%' THEN 'VITAMIN C'
        ELSE NULL
    END AS product_name

FROM raw_messages
