-- Dimensions
create table if not exists dim_date (
    date_key date primary key,
    year int,
    month int,
    day int,
    dow int
);

create table if not exists dim_location (
    location_key serial primary key,
    borough text,
    incident_zip text
);

-- Fact
create table if not exists fact_requests (
    unique_key text primary key,
    date_key date,
    agency text,
    complaint_type text,
    borough text,
    incident_zip text,
    is_closed boolean,
    hours_open double precision,
    sla_met_48h boolean
);

-- Simple refresh logic (idempotent-ish) using staging
with src as (
    select
        unique_key,
        (created_date)::date as date_key,
        agency,
        complaint_type,
        borough,
        incident_zip,
        (closed_date is not null) as is_closed,
        case when closed_date is not null
             then extract(epoch from (closed_date - created_date))/3600.0
             else extract(epoch from (now() - created_date))/3600.0 end as hours_open,
        case when closed_date is not null and (closed_date - created_date) <= interval '48 hours'
             then true else false end as sla_met_48h
    from staging_nyc311
)
insert into fact_requests as f
(unique_key, date_key, agency, complaint_type, borough, incident_zip, is_closed, hours_open, sla_met_48h)
select * from src
on conflict (unique_key) do update set
    date_key = excluded.date_key,
    agency = excluded.agency,
    complaint_type = excluded.complaint_type,
    borough = excluded.borough,
    incident_zip = excluded.incident_zip,
    is_closed = excluded.is_closed,
    hours_open = excluded.hours_open,
    sla_met_48h = excluded.sla_met_48h;
