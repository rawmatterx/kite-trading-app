from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.get_database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency function that yields database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()