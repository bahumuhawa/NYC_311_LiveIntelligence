# Runbook

## Symptoms

- Dashboard stale (>2h), missing data, or Airflow task failures.

## Checks

1. Airflow UI: confirm DAG status, task logs, and SLA misses.
2. Database: run `sql/tests/dq_queries.sql` to see freshness and nulls.
3. API: query Socrata endpoint manually; check rate limits and token.

## Remediation

- Re-run failed tasks with backfill.
- Increase retries or lower PAGE_SIZE during API throttling.
- Escalate to platform team if infra degraded.
