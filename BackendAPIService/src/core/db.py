from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from src.core.config import settings

# SQLAlchemy Base and engine
Base = declarative_base()

# For SQLite, need check_same_thread False if using default
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def get_db() -> Session:
    """Dependency to provide a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create database tables."""
    # Import models to ensure SQLAlchemy registers metadata before creating tables
    from src.models import user as _user  # noqa: F401
    from src.models import kyc as _kyc  # noqa: F401
    from src.models import audit as _audit  # noqa: F401
    Base.metadata.create_all(bind=engine)
