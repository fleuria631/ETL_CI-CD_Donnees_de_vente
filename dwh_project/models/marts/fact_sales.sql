with order_items as (
    select * from {{ ref('stg_sales_order_items') }}
),

orders as (
    select * from {{ ref('stg_sales_orders') }}
),

dim_product as (
    select * from {{ ref('dim_product') }}
),

dim_customer as (
    select * from {{ ref('dim_customer') }}
),

dim_address as (
    select * from {{ ref('dim_address') }}
),

dim_date as (
    select * from {{ ref('dim_date') }}
),

joined as (
    select
        oi.sales_order_item_id,
        oi.sales_order_id,
        o.order_code,
        o.status,
        o.currency,
        o.customer_id,
        oi.product_id,
        cast(o.created_at as date) as order_date,
        oi.quantity,
        oi.quantity_delivered,
        oi.unit_price,
        oi.discount_percent,
        oi.line_total
    from order_items oi
    left join orders o
        on oi.sales_order_id = o.sales_order_id
)

select
    j.sales_order_item_id,
    j.sales_order_id,
    j.order_code,
    j.status,
    j.currency,
    dc.customer_key,
    dp.product_key,
    da.address_key,
    dd.date_key,
    j.quantity,
    j.quantity_delivered,
    j.unit_price,
    j.discount_percent,
    j.line_total
from joined j
left join dim_customer dc
    on j.customer_id = dc.customer_id
left join dim_product dp
    on j.product_id = dp.product_id
left join dim_address da
    on j.customer_id = da.customer_id
left join dim_date dd
    on j.order_date = dd.date_key