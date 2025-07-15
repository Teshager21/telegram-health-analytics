{{ config(
    materialized='table'
) }}

select
    message_id,
    detected_object_class,
    confidence_score
from
    {{ ref('stg_image_detections') }}
