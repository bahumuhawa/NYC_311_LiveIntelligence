# Project Scope

**In Scope**

- Incremental ingestion from NYC 311 Socrata API.
- Postgres-based staging and gold marts.
- Data quality monitoring (freshness, null %, domian checks).
- Power BI dashbords for operations and leadership.

**Out of scope (MVP)**

- ML forecasting, geocoding normalization, PII handling.
- Complex SCD dimensions, cross-agency joins.
- Multi cloud + DR strategy (documented for forture).

**Success Criteria**

- Freshness < 15 minutes
- > 99% DAG success rate.
- < 1% DQ voilations per day.
