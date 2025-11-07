-- Staging table for raw-normalized NYC 311 requests
create table if not exists staging_nyc311 (
    unique_key text primary key,
    created_date timestamptz,
    closed_date timestamptz,
    agency text,
    complaint_type text,
    descriptor text,
    status text,
    borough text,
    incident_zip text,
    latitude double precision,
    longitude double precision,
    resolution_description text,
    updated_date timestamptz
);
