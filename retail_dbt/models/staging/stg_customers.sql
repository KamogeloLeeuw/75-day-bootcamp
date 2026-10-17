with source as (
    select * from {{ source('retail_shop', 'customers') }}
),

renamed as (
    select
        customer_id,
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        lower(trim(email)) as email,
        trim(city) as city,
        join_date::date as join_date
    from source
    where customer_id is not null
)

select * from renamed