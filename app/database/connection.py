from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL


if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured in .env"
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Create database session for each request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()