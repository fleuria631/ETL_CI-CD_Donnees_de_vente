with customer_address as (
    select * from {{ ref('int_customer_address') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as address_key,
    customer_id,
    street,
    city,
    raw_address
from customer_address