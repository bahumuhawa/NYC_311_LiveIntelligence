from datetime import datetime

def to_float(v):
    try:
        return float(v) if v is not None else None
    except Exception:
        return None


def normalize(row: dict) -> dict:
    # Basic field mapping with light typing.
    created = row.get("created_date")
    closed = row.get("closed_date")
    return {
        "unique_key": row.get("unique_key"),
        "created_date": created,
        "closed_date": closed,
        "agency": row.get("agency"),
        "complaint_type": row.get("complaint_type"),
        "descriptor": row.get("descriptor"),
        "status": row.get("status"),
        "borough": row.get("borough"),
        "incident_zip": row.get("incident_zip"),
        "latitude": to_float(row.get("latitude")),
        "longitude": to_float(row.get("longitude")),
        "resolution_description": row.get("resolution_description"),
        "updated_date": row.get("closed_date") or row.get("created_date"),
    }
