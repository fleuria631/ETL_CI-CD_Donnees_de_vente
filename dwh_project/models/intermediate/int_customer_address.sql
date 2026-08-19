with customers as (
    select * from {{ ref('stg_customers') }}
),

parsed as (
    select
        customer_id,
        address as raw_address,
        trim(split_part(address, ',', 1)) as street,
        trim(split_part(address, ',', 2)) as city
    from customers
)

select
    customer_id,
    raw_address,
    street,
    city
from parsed