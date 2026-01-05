"""Account model for trader portfolios."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, Float, JSON, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Account(Base):
    """Account model representing a trader's portfolio."""
    
    __tablename__ = "accounts"
    
    # Basic account info
    name = Column(String(50), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=True)
    balance = Column(Float, default=10000.0, nullable=False)
    
    # Trading configuration
    is_active = Column(Boolean, default=True, nullable=False)
    strategy_id = Column(String(36), nullable=True)  # Foreign key to strategy
    
    # Portfolio data (stored as JSON for flexibility)
    holdings = Column(JSON, default=dict, nullable=False)  # {symbol: quantity}
    portfolio_value_history = Column(JSON, default=list, nullable=False)  # [(timestamp, value)]
    
    # Performance metrics
    total_portfolio_value = Column(Float, default=0.0, nullable=False)
    total_profit_loss = Column(Float, default=0.0, nullable=False)
    win_rate = Column(Float, default=0.0, nullable=False)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    logs = relationship("AgentLog", back_populates="account", cascade="all, delete-orphan")
    snapshots = relationship("PortfolioSnapshot", back_populates="account", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Account(name='{self.name}', balance={self.balance}, portfolio_value={self.total_portfolio_value})>"
    
    def calculate_portfolio_value(self, market_prices: dict[str, float]) -> float:
        """Calculate current portfolio value based on market prices."""
        holdings_value = sum(
            quantity * market_prices.get(symbol, 0.0) 
            for symbol, quantity in self.holdings.items()
        )
        return self.balance + holdings_value
    
    def update_portfolio_value(self, new_value: float) -> None:
        """Update portfolio value and add to history."""
        self.total_portfolio_value = new_value
        timestamp = datetime.utcnow().isoformat()
        
        # Add to history (keep last 1000 entries)
        if not isinstance(self.portfolio_value_history, list):
            self.portfolio_value_history = []
            
        self.portfolio_value_history.append([timestamp, new_value])
        if len(self.portfolio_value_history) > 1000:
            self.portfolio_value_history = self.portfolio_value_history[-1000:]
    
    def add_holding(self, symbol: str, quantity: int) -> None:
        """Add shares to holdings."""
        if not isinstance(self.holdings, dict):
            self.holdings = {}
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
    
    def remove_holding(self, symbol: str, quantity: int) -> bool:
        """Remove shares from holdings. Returns True if successful."""
        if not isinstance(self.holdings, dict):
            self.holdings = {}
            
        current_quantity = self.holdings.get(symbol, 0)
        if current_quantity >= quantity:
            self.holdings[symbol] = current_quantity - quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            return True
        return False