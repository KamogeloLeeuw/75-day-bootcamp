-- calculating the total spent, order count, and average order value per customer

with enriched as (
    select * from {{ ref('int_order_items_enriched') }}
),

customer_orders as (
    select
        customer_id,
        customer_first_name,
        customer_last_name,
        customer_city,
        count(distinct order_id) as total_orders,
        sum(line_total) as life_time_value,
        round(avg(line_total), 2) as avg_order_item_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date
    from enriched
    group by 1, 2, 3, 4
)

select * from customer_orders
order by life_time_value desc

