with source as (
    select * from {{ source('retail_shop', 'order_items') }}
),

renamed as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price::numeric(10,2) as unit_price,
        (quantity * unit_price)::numeric(10,2) as line_total
    from source
    where order_item_id is not null
)

select * from renamed