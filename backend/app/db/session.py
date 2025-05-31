from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine
engine = None
SessionLocal = None

# Create session factory
def init_db():
    global engine, SessionLocal
    
    if engine is None:
        database_url = settings.get_database_url
        logger.info(f"Connecting to database: {database_url}")
        
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,  # Recycle connections after 5 minutes
            pool_size=5,
            max_overflow=10,
            echo=settings.DEBUG
        )
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database when the module is imported
init_db()

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency function that yields database sessions."""
    if SessionLocal is None:
        init_db()
        
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()