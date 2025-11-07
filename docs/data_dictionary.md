# Data Dictionary (Staging)

- `unique_key` (text): Unique request id.
- `created_date` (timestampz): when he request was created.
- `closed_date` (timestampz): When the request was closed.
- `agency` (text): Responsible agency.
- ` complaint_type` (text): Category of request.
- `descriptor` (text): Subcatergory / details.
- `status` (text): Open/Closed/Assigned.
- ` borough` (text): NYC Borough.
- `incident_zip`(text): ZIP code of incident.
- `latitude`, ` longitude` (double): Geolocation.
- `resolution_description` (text): Resolution notes.
- `updated_date` (timestampz): Last update timestamp (Fallback = created).
