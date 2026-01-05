"""Account management API endpoints."""

from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ...core.database import get_db
from ...services.account_service import AccountService
from ...services.market_service import MarketService


router = APIRouter()


class AccountSummary(BaseModel):
    """Account summary response model."""
    name: str
    display_name: str
    balance: float
    holdings: Dict[str, int]
    total_portfolio_value: float
    total_profit_loss: float
    win_rate: float


class TransactionResponse(BaseModel):
    """Transaction response model."""
    symbol: str
    transaction_type: str
    quantity: int
    price: float
    created_at: str
    rationale: str = None


@router.get("/", response_model=List[AccountSummary])
async def get_all_accounts(db: Session = Depends(get_db)):
    """Get all trading accounts with current status."""
    account_service = AccountService(db)
    market_service = MarketService(db)
    
    accounts = account_service.get_all_accounts()
    summaries = []
    
    for account in accounts:
        # Get current market prices for portfolio calculation
        symbols = list(account.holdings.keys()) if account.holdings else []
        market_prices = market_service.get_multiple_prices(symbols)
        current_value = account_service.calculate_portfolio_value(account, market_prices)
        
        summary = AccountSummary(
            name=account.name,
            display_name=account.display_name or account.name.title(),
            balance=account.balance,
            holdings=account.holdings or {},
            total_portfolio_value=current_value,
            total_profit_loss=current_value - 10000.0,  # Assuming $10k initial
            win_rate=account.win_rate or 0.0
        )
        summaries.append(summary)
    
    return summaries


@router.get("/{account_name}", response_model=AccountSummary)
async def get_account(account_name: str, db: Session = Depends(get_db)):
    """Get specific account details."""
    account_service = AccountService(db)
    market_service = MarketService(db)
    
    account = account_service.get_account_by_name(account_name)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account '{account_name}' not found")
    
    # Get current market prices for portfolio calculation
    symbols = list(account.holdings.keys()) if account.holdings else []
    market_prices = market_service.get_multiple_prices(symbols)
    current_value = account_service.calculate_portfolio_value(account, market_prices)
    
    return AccountSummary(
        name=account.name,
        display_name=account.display_name or account.name.title(),
        balance=account.balance,
        holdings=account.holdings or {},
        total_portfolio_value=current_value,
        total_profit_loss=current_value - 10000.0,  # Assuming $10k initial
        win_rate=account.win_rate or 0.0
    )


@router.get("/{account_name}/transactions", response_model=List[TransactionResponse])
async def get_account_transactions(
    account_name: str, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """Get transaction history for an account."""
    account_service = AccountService(db)
    
    account = account_service.get_account_by_name(account_name)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account '{account_name}' not found")
    
    transactions = account_service.get_account_transactions(account.id, limit)
    
    return [
        TransactionResponse(
            symbol=t.symbol,
            transaction_type=t.transaction_type.value,
            quantity=abs(t.quantity),
            price=t.price,
            created_at=t.created_at.isoformat(),
            rationale=t.rationale
        )
        for t in transactions
    ]


@router.get("/{account_name}/portfolio-history")
async def get_portfolio_history(account_name: str, db: Session = Depends(get_db)):
    """Get portfolio value history for charting."""
    account_service = AccountService(db)
    
    account = account_service.get_account_by_name(account_name)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account '{account_name}' not found")
    
    history = account.portfolio_value_history or []
    
    return {
        "account_name": account_name,
        "history": [
            {"timestamp": entry[0], "value": entry[1]}
            for entry in history
        ]
    }


@router.post("/{account_name}/reset")
async def reset_account(
    account_name: str, 
    strategy: str = None,
    db: Session = Depends(get_db)
):
    """Reset an account to initial state."""
    account_service = AccountService(db)
    
    account = account_service.get_account_by_name(account_name)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account '{account_name}' not found")
    
    reset_account = account_service.reset_account(account.id, strategy)
    
    return {
        "message": f"Account '{account_name}' has been reset",
        "new_balance": reset_account.balance,
        "strategy": strategy
    }