with products as (
    select * from {{ ref('stg_products') }}
),

categories as (
    select * from {{ ref('stg_categories') }}
),

joined as (
    select
        p.product_id,
        p.product_name,
        p.product_code,
        p.is_active,
        p.license_duration_type,
        p.license_duration_days,
        p.delivery_type,
        c.category_id,
        c.category_name,
        c.category_slug
    from products p
    left join categories c
        on p.category_id = c.category_id
)

select
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_key,
    product_id,
    product_name,
    product_code,
    is_active,
    license_duration_type,
    license_duration_days,
    delivery_type,
    category_id,
    category_name,
    category_slug
from joined