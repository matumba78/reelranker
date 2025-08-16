from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import time
import logging
from typing import Generator
from contextlib import contextmanager

from app.core.config import settings
from app.models.video import Base

logger = logging.getLogger(__name__)

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_pre_ping=True,  # Verify connections before use
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Get database session with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

@contextmanager
def get_db_context():
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db(max_retries: int = 3, retry_delay: float = 1.0) -> bool:
    """Initialize database with retry logic"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to initialize database (attempt {attempt + 1}/{max_retries})")
            
            # Test connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            # Create tables
            Base.metadata.create_all(bind=engine)
            
            logger.info("Database initialized successfully")
            return True
            
        except OperationalError as e:
            logger.warning(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
            else:
                logger.error("Failed to initialize database after all retries")
                return False
        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            return False

def check_db_health() -> bool:
    """Check if database is healthy"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

def close_db_connections():
    """Close all database connections"""
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")
