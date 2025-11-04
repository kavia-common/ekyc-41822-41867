import os
from functools import lru_cache
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""

    # Container-provided variables (do not guess values; orchestrator sets .env)
    PGAPI_BASE: Optional[str] = os.getenv("PGAPI_BASE")
    PGBACKEND_URL: Optional[str] = os.getenv("PGBACKEND_URL")
    PGFRONTEND_URL: Optional[str] = os.getenv("PGFRONTEND_URL")
    PGWS_URL: Optional[str] = os.getenv("PGWS_URL")
    PGNODE_ENV: str = os.getenv("PGNODE_ENV", "development")
    PGENABLE_SOURCE_MAPS: Optional[str] = os.getenv("PGENABLE_SOURCE_MAPS")
    PGPORT: int = int(os.getenv("PGPORT", "8000"))
    PGTRUST_PROXY: Optional[str] = os.getenv("PGTRUST_PROXY")
    PGLOG_LEVEL: str = os.getenv("PGLOG_LEVEL", "INFO")
    PGHEALTHCHECK_PATH: str = os.getenv("PGHEALTHCHECK_PATH", "/")
    PGFEATURE_FLAGS: Optional[str] = os.getenv("PGFEATURE_FLAGS")
    PGEXPERIMENTS_ENABLED: Optional[str] = os.getenv("PGEXPERIMENTS_ENABLED")

    # Database URL (use standard SQLAlchemy DATABASE_URL variable pattern)
    # Expect the orchestrator to provide DATABASE_URL, preferably PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ekyc.db")

    # Security settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-in-env")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Storage
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "./storage")
    os.makedirs(STORAGE_DIR, exist_ok=True)

    # Audit
    AUDIT_LOG_FILE: str = os.getenv("AUDIT_LOG_FILE", "./storage/audit.log")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Single shared settings instance
settings = get_settings()
