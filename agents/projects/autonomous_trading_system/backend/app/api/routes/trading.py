"""Trading API endpoints."""

from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.trading_service import TradingService


router = APIRouter()


class TradeRequest(BaseModel):
    """Trade request model."""
    symbol: str
    quantity: int
    rationale: str = None


class TradeResponse(BaseModel):
    """Trade response model."""
    success: bool
    symbol: str
    quantity: int
    total_cost: float = None
    total_proceeds: float = None
    new_balance: float
    portfolio_value: float


@router.post("/{account_name}/buy", response_model=TradeResponse)
async def buy_shares(
    account_name: str,
    trade_request: TradeRequest,
    db: Session = Depends(get_db)
):
    """Execute a buy order."""
    trading_service = TradingService(db)
    
    try:
        result = trading_service.execute_buy_order(
            account_name=account_name,
            symbol=trade_request.symbol,
            quantity=trade_request.quantity,
            rationale=trade_request.rationale
        )
        
        return TradeResponse(
            success=result["success"],
            symbol=result["symbol"],
            quantity=result["quantity"],
            total_cost=result["total_cost"],
            new_balance=result["new_balance"],
            portfolio_value=result["portfolio_value"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trading error: {str(e)}")


@router.post("/{account_name}/sell", response_model=TradeResponse)
async def sell_shares(
    account_name: str,
    trade_request: TradeRequest,
    db: Session = Depends(get_db)
):
    """Execute a sell order."""
    trading_service = TradingService(db)
    
    try:
        result = trading_service.execute_sell_order(
            account_name=account_name,
            symbol=trade_request.symbol,
            quantity=trade_request.quantity,
            rationale=trade_request.rationale
        )
        
        return TradeResponse(
            success=result["success"],
            symbol=result["symbol"],
            quantity=result["quantity"],
            total_proceeds=result["total_proceeds"],
            new_balance=result["new_balance"],
            portfolio_value=result["portfolio_value"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trading error: {str(e)}")


@router.get("/{account_name}/summary")
async def get_trading_summary(account_name: str, db: Session = Depends(get_db)):
    """Get comprehensive trading summary for an account."""
    trading_service = TradingService(db)
    
    try:
        summary = trading_service.get_trading_summary(account_name)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary error: {str(e)}")


@router.get("/summary")
async def get_all_trading_summaries(db: Session = Depends(get_db)):
    """Get trading summaries for all accounts."""
    trading_service = TradingService(db)
    
    try:
        summaries = trading_service.get_all_accounts_summary()
        return {
            "accounts": summaries,
            "total_accounts": len(summaries),
            "timestamp": "2025-01-01T00:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary error: {str(e)}")