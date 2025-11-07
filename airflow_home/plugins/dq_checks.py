from datetime import timedelta
import psycopg2
from psycopg2 import sql
from airflow.exceptions import AirflowException
from ingestion.config import settings

def run_basic_dq_checks(
    schema: str = "public",
    table: str = "staging_nyc311",
    max_freshness_minutes: int = 120,
) -> None:
    issues = []

    with psycopg2.connect(settings.pg_dsn) as conn:
        with conn.cursor() as cur:
            # optional: keep queries snappy
            cur.execute("SET statement_timeout = '30s';")

            tbl = sql.Identifier(schema, table)

            # 1) Freshness: MAX(created_date) must be within N minutes
            cur.execute(
                sql.SQL("""
                    SELECT
                        MAX(created_date) AS max_created,
                        EXTRACT(EPOCH FROM (NOW() - MAX(created_date)))::bigint AS lag_seconds
                    FROM {}""").format(tbl)
            )
            max_created, lag_seconds = cur.fetchone()

            # If table empty or no created_date yet
            if max_created is None:
                issues.append("No data found in staging (MAX(created_date) is NULL).")
            else:
                if lag_seconds is None or lag_seconds > max_freshness_minutes * 60:
                    issues.append(
                        f"Freshness lag too high: {lag_seconds}s "
                        f"(threshold {max_freshness_minutes*60}s, max_created={max_created})."
                    )

            # 2) Not-null check on unique_key
            cur.execute(
                sql.SQL("""
                    SELECT COUNT(*) FROM {} WHERE unique_key IS NULL
                """).format(tbl)
            )
            nulls = cur.fetchone()[0]
            if nulls and nulls > 0:
                issues.append(f"Null unique_key rows: {nulls}")

    if issues:
        # Make the Airflow task fail with a clear message
        raise AirflowException("; ".join(issues))
