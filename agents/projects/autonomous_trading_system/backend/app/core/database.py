"""Database connection and session management."""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .config import settings
from ..models.base import Base


# Create database engine
if settings.database_url.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        settings.database_url,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
        echo=settings.debug
    )
    
    # Enable foreign key constraints for SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if 'sqlite' in str(dbapi_connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
else:
    # PostgreSQL or other databases
    engine = create_engine(
        settings.database_url,
        echo=settings.debug
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager to get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class DatabaseManager:
    """Database management utilities."""
    
    @staticmethod
    def init_database():
        """Initialize database with tables and default data."""
        create_tables()
        DatabaseManager.create_default_data()
    
    @staticmethod
    def create_default_data():
        """Create default strategies and accounts."""
        from ..models.strategy import Strategy
        from ..models.account import Account
        
        with get_db_session() as db:
            # Create default strategies if they don't exist
            if not db.query(Strategy).filter(Strategy.name == "warren_patience").first():
                warren_strategy = Strategy.create_warren_strategy()
                db.add(warren_strategy)
            
            if not db.query(Strategy).filter(Strategy.name == "george_bold").first():
                george_strategy = Strategy.create_george_strategy()
                db.add(george_strategy)
            
            # Create default accounts if they don't exist
            default_accounts = [
                ("warren", "Warren", "warren_patience"),
                ("george", "George", "george_bold"),
                ("ray", "Ray", None),
                ("cathie", "Cathie", None),
            ]
            
            for name, display_name, strategy_name in default_accounts:
                if not db.query(Account).filter(Account.name == name).first():
                    account = Account(
                        name=name,
                        display_name=display_name,
                        balance=settings.initial_balance,
                        strategy_id=strategy_name
                    )
                    db.add(account)
    
    @staticmethod
    def reset_database():
        """Reset database by dropping and recreating all tables."""
        drop_tables()
        create_tables()
        DatabaseManager.create_default_data()
    
    @staticmethod
    def backup_database(backup_path: str):
        """Backup database to specified path."""
        if settings.database_url.startswith("sqlite"):
            import shutil
            db_path = settings.database_url.replace("sqlite:///", "")
            shutil.copy2(db_path, backup_path)
        else:
            # For other databases, would need pg_dump or similar
            raise NotImplementedError("Backup not implemented for non-SQLite databases")
    
    @staticmethod
    def get_database_stats():
        """Get database statistics."""
        from ..models import Account, Transaction, MarketData, AgentLog
        
        with get_db_session() as db:
            return {
                "accounts": db.query(Account).count(),
                "transactions": db.query(Transaction).count(),
                "market_data_records": db.query(MarketData).count(),
                "log_entries": db.query(AgentLog).count(),
            }