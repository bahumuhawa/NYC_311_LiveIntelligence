-- Freshness: latest created_date within last 2 hours
select now() - max(created_date) as freshness_lag from staging_nyc311;

-- Required fields not null
select count(*) as null_unique_keys from staging_nyc311 where unique_key is null;

-- Borough domain check
select borough, count(*) from staging_nyc311
where borough not in ('BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND') and borough is not null
group by 1;
