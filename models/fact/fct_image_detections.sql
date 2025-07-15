{{ config(
    materialized='table'
) }}

select
    message_id,
    detected_object_class,
    confidence_score
from
    raw.fct_image_detections
