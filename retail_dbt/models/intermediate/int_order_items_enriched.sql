-- int_order_items_enriched.sql
-- Joins order items with order, customers, products and employees
-- Creating one enriched row per order item

with order_items as (
    select * from {{ref ('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref ('stg_customers')}}
),

products as (
    select * from {{ ref ('stg_products')}}
),

employees as (
    select * from {{ ref ('stg_employees')}}
),

enriched as (
    select
        oi.order_item_id,
        oi.order_id,
        oi.product_id,
        oi.quantity,
        oi.unit_price,
        oi.line_total,

        o.order_date,
        o.status as order_status,

        c.customer_id,
        c.first_name as customer_first_name,
        c.last_name as customer_last_name,
        c.city as customer_city,

        p.product_name,
        p.price as listed_price,
        p.category_id,

        e.employee_id,
        e.first_name as employee_first_name,
        e.last_name as employee_last_name,
        e.position as employee_position


    from order_items oi
    left join orders o on oi.order_id = o.order_id
    left join customers c on o.customer_id = c.customer_id
    left join products p on oi.product_id = p.product_id
    left join employees e on o.employee_id = e.employee_id

)

select * from enriched