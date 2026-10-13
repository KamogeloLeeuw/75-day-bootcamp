with source as (
    select * from {{ source('retail_shop', 'products') }}
),

renamed as (
    select
        product_id,
        category_id,
        trim(product_name) as product_name,
        price::numeric(10,2) as price,
        stock_quantity
    from source
    where product_id is not null
)

select * from renamed