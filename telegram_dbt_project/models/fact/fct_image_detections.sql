{{ config(
    materialized='table'
) }}

with detections as (
    select
        message_id,
        detected_object_class,
        confidence_score
    from {{ ref('stg_image_detections') }}
),

valid_messages as (
    select message_id from {{ ref('fct_messages') }}
)

select
    d.message_id,
    d.detected_object_class,
    d.confidence_score
from detections d
inner join valid_messages vm
    on d.message_id = vm.message_id
