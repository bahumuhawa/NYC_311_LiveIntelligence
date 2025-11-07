import os
from pydantic import BaseModel


class Settings(BaseModel):
    SOCRATA_BASE: str = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    SOCRATA_APP_TOKEN: str | None = os.getenv("SOCRATA_APP_TOKEN")

    PG_HOST: str = os.getenv("PG_HOST", "localhost")
    PG_PORT: int = int(os.getenv("PG_PORT", "5432"))
    PG_DB: str = os.getenv("PG_DB", "nyc311")
    PG_USER: str = os.getenv("PG_USER", "postgres")
    PG_PASSWORD: str = os.getenv("PG_PASSWORD", "postgres")

    LAST_WATERMARK_ISO: str = os.getenv("LAST_WATERMARK_ISO", "2025-01-01T00:00:00Z")
    PAGE_SIZE: int = int(os.getenv("PAGE_SIZE", "50000"))
    SLA_HOURS: int = int(os.getenv("SLA_HOURS", "48"))

    @property
    def pg_dsn(self) -> str:
        return (
            f"host={self.PG_HOST} "
            f"port={self.PG_PORT} "
            f"dbname={self.PG_DB} "
            f"user={self.PG_USER} "
            f"password={self.PG_PASSWORD}"
        )


settings = Settings()
