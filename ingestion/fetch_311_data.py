import os, time, requests, json
import psycopg2
from psycopg2.extras import execute_batch
from ingestion.config import settings
from ingestion.normalize import normalize


def fetch_incremental(since_iso: str):
    headers = (
        {"X-App-Token": settings.SOCRATA_APP_TOKEN}
        if settings.SOCRATA_APP_TOKEN
        else {}
    )
    where = f"created_date > '{since_iso}'"
    order = "created_date"
    offset = 0
    all_rows = []

    while True:
        params = {
            "$where": where,
            "$order": order,
            "$limit": settings.PAGE_SIZE,
            "$offset": offset,
        }
        # Use the Socrata BASE URL, not the token
        r = requests.get(
            settings.SOCRATA_BASE, params=params, headers=headers, timeout=60
        )
        r.raise_for_status()
        batch = r.json()

        if not batch:
            break

        all_rows.extend(batch)
        offset += len(batch)
        time.sleep(0.2)

    return all_rows


def ensure_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS staging_nyc311 (
                unique_key TEXT PRIMARY KEY,
                created_date TIMESTAMPTZ,
                closed_date TIMESTAMPTZ,
                agency TEXT,
                complaint_type TEXT,
                descriptor TEXT,
                status TEXT,
                borough TEXT,
                incident_zip TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                resolution_description TEXT,
                updated_date TIMESTAMPTZ
            );
        """
        )
    conn.commit()


def upsert_rows(conn, rows):
    sql = """
        INSERT INTO staging_nyc311
        (unique_key, created_date, closed_date, agency, complaint_type, descriptor, status, borough, incident_zip,
         latitude, longitude, resolution_description, updated_date)
        VALUES (%(unique_key)s, %(created_date)s, %(closed_date)s, %(agency)s, %(complaint_type)s, %(descriptor)s,
                %(status)s, %(borough)s, %(incident_zip)s, %(latitude)s, %(longitude)s, %(resolution_description)s,
                %(updated_date)s)
        ON CONFLICT (unique_key) DO UPDATE SET
            created_date = EXCLUDED.created_date,
            closed_date = EXCLUDED.closed_date,
            agency = EXCLUDED.agency,
            complaint_type = EXCLUDED.complaint_type,
            descriptor = EXCLUDED.descriptor,
            status = EXCLUDED.status,
            borough = EXCLUDED.borough,
            incident_zip = EXCLUDED.incident_zip,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            resolution_description = EXCLUDED.resolution_description,
            updated_date = EXCLUDED.updated_date;
    """
    with conn.cursor() as cur:
        execute_batch(cur, sql, rows, page_size=1000)
    conn.commit()


def main():
    raw = fetch_incremental(settings.LAST_WATERMARK_ISO)
    rows = [normalize(r) for r in raw]
    print(f"Fetched {len(rows)} rows since {settings.LAST_WATERMARK_ISO}")

    conn = psycopg2.connect(settings.pg_dsn)
    ensure_tables(conn)

    if rows:
        upsert_rows(conn, rows)
        print("Upsert complete.")

    conn.close()


if __name__ == "__main__":
    main()
