select
    id as customer_id,
    user_id,
    first_name,
    last_name,
    phone,
    address,
    customer_type,
    company_name,
    nif,
    rcs,
    stat,
    vat_number,
    company_number,
    utr_number,
    created_at,
    updated_at,
    extracted_at
from {{ source('dwh', 'customers') }}