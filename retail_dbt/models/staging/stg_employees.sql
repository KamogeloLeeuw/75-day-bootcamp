with source as (
    select * from {{ source('retail_shop', 'employees')}}
),

renamed as (
    select
        employee_id,
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        trim(position) as position,
        salary::numeric(10,2) as salary
    from source
    where employee_id is not null

)

select * from renamed