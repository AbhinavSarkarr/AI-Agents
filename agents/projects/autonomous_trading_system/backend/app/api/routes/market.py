"""Market data API endpoints."""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.market_service import MarketService


router = APIRouter()


class PriceResponse(BaseModel):
    """Stock price response model."""
    symbol: str
    price: float
    timestamp: str


class MarketSummaryResponse(BaseModel):
    """Market summary response model."""
    date: str
    market_open: bool
    symbols_updated_today: int
    polygon_api_available: bool
    polygon_plan: str
    data_sources: List[str]


@router.get("/price/{symbol}", response_model=PriceResponse)
async def get_stock_price(symbol: str, db: Session = Depends(get_db)):
    """Get current price for a specific stock symbol."""
    market_service = MarketService(db)
    
    try:
        price = market_service.get_share_price(symbol.upper())
        
        return PriceResponse(
            symbol=symbol.upper(),
            price=price,
            timestamp="2025-01-01T00:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price fetch error: {str(e)}")


@router.post("/prices", response_model=Dict[str, float])
async def get_multiple_prices(symbols: List[str], db: Session = Depends(get_db)):
    """Get prices for multiple stock symbols."""
    market_service = MarketService(db)
    
    try:
        # Convert to uppercase and remove duplicates
        clean_symbols = list(set(symbol.upper() for symbol in symbols))
        prices = market_service.get_multiple_prices(clean_symbols)
        
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prices fetch error: {str(e)}")


@router.get("/summary", response_model=MarketSummaryResponse)
async def get_market_summary(db: Session = Depends(get_db)):
    """Get market data summary and status."""
    market_service = MarketService(db)
    
    try:
        summary = market_service.get_market_summary()
        
        return MarketSummaryResponse(
            date=summary["date"],
            market_open=summary["market_open"],
            symbols_updated_today=summary["symbols_updated_today"],
            polygon_api_available=summary["polygon_api_available"],
            polygon_plan=summary["polygon_plan"],
            data_sources=summary["data_sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market summary error: {str(e)}")


@router.get("/status")
async def get_market_status(db: Session = Depends(get_db)):
    """Get current market status."""
    market_service = MarketService(db)
    
    return {
        "market_open": market_service.is_market_open(),
        "timestamp": "2025-01-01T00:00:00Z"
    }