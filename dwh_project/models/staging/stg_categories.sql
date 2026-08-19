select
    id as category_id,
    name as category_name,
    slug as category_slug,
    parent_id as parent_category_id,
    active as is_active,
    extracted_at
from {{ source('dwh', 'categories') }}