-- stg_orders.sql
-- Staging model for order tables
-- Renaming columns, casts types, and filters out invalid row

with source as (
    select * from {{ source('retail_shop', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        employee_id,
        order_date::date as order_date,
        lower(trim(status)) as status
    from source
    where order_id is not null
)

select * from renamed