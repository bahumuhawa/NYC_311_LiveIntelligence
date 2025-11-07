from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.utils.email import send_email
from airflow.models import Variable

from ingestion.fetch_311_data import main as ingest_main
from monitoring.dq_checks import run_basic_dq_checks  # <-- import directly

def on_failure_callback(context):
    subject = f"Airflow DAG {context['dag'].dag_id} failed"
    html_content = f"Task {context['task_instance'].task_id} failed at {datetime.utcnow()}"
    to = Variable.get("ALERT_EMAIL", default_var=None)
    if to:
        send_email(to=to, subject=subject, html_content=html_content)

# Prefer `schedule` (new) over `schedule_interval`
with DAG(
    dag_id="nyc311_incremental",
    description="Incremental NYC 311 ingestion with DQ checks and gold build",
    schedule="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={
        "owner": "data-eng",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": False,
        "on_failure_callback": on_failure_callback,
    },
    tags=["nyc311", "ingestion"],
) as dag:

    ingest = PythonOperator(
        task_id="ingest_staging",
        python_callable=ingest_main,
    )

    dq_checks_task = PythonOperator(
        task_id="dq_checks",
        python_callable=run_basic_dq_checks,
    )

    def build_gold():
        # Execute gold DDL/refresh SQL
        import psycopg2
        from ingestion.config import settings

        sql_path = Variable.get(
            "GOLD_SQL_PATH",
            default_var="/opt/airflow/sql/ddl/gold_tables.sql"  # works in docker if you mount ./sql -> /opt/airflow/sql
        )
        sql_path = Path(sql_path)

        with psycopg2.connect(settings.pg_dsn) as conn:
            with conn.cursor() as cur, sql_path.open("r", encoding="utf-8") as f:
                cur.execute(f.read())
                conn.commit()

    build_gold_task = PythonOperator(
        task_id="build_gold",
        python_callable=build_gold,
    )

    ingest >> dq_checks_task >> build_gold_task
