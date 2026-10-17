-- summary of sales by month, product, and employee
-- materialized as a table for query performance

with enriched as (
    select * from {{ ref('int_order_items_enriched') }}
),

monthly_sales as (
    select
        date_trunc('month', order_date) as month,
        count(distinct order_id) as total_orders,
        sum(line_total) as total_revenue,
        round(avg(line_total), 2) as avg_order_item_value
    from enriched
    where order_status = 'completed'
    group by 1

),

sales_by_employee as (
    select 
        employee_id,
        employee_first_name,
        employee_last_name,
        employee_position,
        count(distinct order_id) as orders_processed,
        sum(line_total) as total_sales,
        round(avg(line_total), 2) as avg_sale_value
    from enriched
    where order_status = 'completed'
    group by 1, 2, 3, 4
),

final as (
    select
        e.employee_first_name,
        e.employee_last_name,
        e.employee_position,
        e.orders_processed,
        e.total_sales,
        e.avg_sale_value
    from sales_by_employee e

)

select * from final
order by total_sales desc
