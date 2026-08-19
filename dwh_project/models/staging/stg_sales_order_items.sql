select
    id as sales_order_item_id,
    sales_order_id,
    product_id,
    variant_id,
    quotation_item_id,
    quantity,
    quantity_delivered,
    unit_price,
    discount_percent,
    line_total,
    description,
    extracted_at
from {{ source('dwh', 'sales_order_items') }}