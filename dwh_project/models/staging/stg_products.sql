select
    id as product_id,
    category_id,
    name as product_name,
    description,
    long_description,
    image_url,
    video_url,
    install_guide_pdf_url,
    active as is_active,
    code as product_code,
    license_duration_type,
    license_duration_days,
    delivery_type,
    extracted_at
from {{ source('dwh', 'products') }}