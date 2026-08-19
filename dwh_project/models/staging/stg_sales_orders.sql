select
    id as sales_order_id,
    code as order_code,
    customer_id,
    quotation_id,
    status,
    customer_po_ref,
    total_amount,
    currency,
    notes,
    confirmed_at,
    created_at,
    updated_at,
    extracted_at
from {{ source('dwh', 'sales_orders') }}