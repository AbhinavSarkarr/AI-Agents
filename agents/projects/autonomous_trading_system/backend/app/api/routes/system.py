"""System management API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db, DatabaseManager
from ...core.config import settings


router = APIRouter()


class SystemStatus(BaseModel):
    """System status response model."""
    status: str
    version: str
    database_connected: bool
    polygon_api_configured: bool
    total_accounts: int
    total_transactions: int


@router.get("/status", response_model=SystemStatus)
async def get_system_status(db: Session = Depends(get_db)):
    """Get overall system status and health."""
    try:
        # Get database statistics
        stats = DatabaseManager.get_database_stats()
        
        return SystemStatus(
            status="healthy",
            version="1.0.0",
            database_connected=True,
            polygon_api_configured=bool(settings.polygon_api_key),
            total_accounts=stats.get("accounts", 0),
            total_transactions=stats.get("transactions", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System status error: {str(e)}")


@router.get("/config")
async def get_system_config():
    """Get system configuration (non-sensitive values only)."""
    return {
        "polygon_plan": settings.polygon_plan,
        "polygon_api_configured": bool(settings.polygon_api_key),
        "run_every_n_minutes": settings.run_every_n_minutes,
        "run_even_when_market_is_closed": settings.run_even_when_market_is_closed,
        "use_many_models": settings.use_many_models,
        "initial_balance": settings.initial_balance,
        "spread": settings.spread,
        "debug": settings.debug
    }


@router.post("/reset-database")
async def reset_database():
    """Reset the entire database (WARNING: This will delete all data!)."""
    try:
        DatabaseManager.reset_database()
        return {
            "message": "Database has been reset successfully",
            "warning": "All previous data has been deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database reset error: {str(e)}")


@router.get("/database-stats")
async def get_database_stats():
    """Get detailed database statistics."""
    try:
        stats = DatabaseManager.get_database_stats()
        return {
            "statistics": stats,
            "timestamp": "2025-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database stats error: {str(e)}")


@router.post("/initialize")
async def initialize_system():
    """Initialize or reinitialize the system."""
    try:
        DatabaseManager.init_database()
        return {
            "message": "System initialized successfully",
            "database": "ready",
            "accounts": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System initialization error: {str(e)}")