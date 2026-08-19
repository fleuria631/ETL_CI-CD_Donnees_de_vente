with customers as (
    select * from {{ ref('stg_customers') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,
    customer_id,
    first_name,
    last_name,
    phone,
    customer_type,
    company_name,
    created_at as customer_since
from customers