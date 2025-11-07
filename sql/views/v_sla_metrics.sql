create or replace view v_sla_metrics as
select
  date_key,
  borough,
  complaint_type,
  count(*) as total_requests,
  sum(case when is_closed then 1 else 0 end) as closed_requests,
  avg(hours_open) as avg_resolution_hours,
  avg(case when sla_met_48h then 1.0 else 0.0 end) as sla_met_pct
from fact_requests
group by 1,2,3;
