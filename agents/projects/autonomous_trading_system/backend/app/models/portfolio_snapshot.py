"""Portfolio snapshot model for tracking portfolio state over time."""

from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Float, JSON, String
from sqlalchemy.orm import relationship

from .base import Base


class PortfolioSnapshot(Base):
    """Portfolio snapshot model for tracking portfolio state at specific points in time."""
    
    __tablename__ = "portfolio_snapshots"
    
    # Basic snapshot info
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    snapshot_type = Column(String(20), default="daily", nullable=False)  # daily, weekly, monthly, trade
    
    # Portfolio metrics at snapshot time
    total_value = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    invested_value = Column(Float, nullable=False)
    
    # Performance metrics
    total_return = Column(Float, nullable=True)  # Since inception
    daily_return = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)
    
    # Holdings breakdown (stored as JSON)
    holdings = Column(JSON, nullable=False)  # {symbol: {quantity, value, weight}}
    sector_allocation = Column(JSON, nullable=True)  # {sector: weight}
    
    # Market context
    market_data = Column(JSON, nullable=True)  # Market indices, VIX, etc.
    
    # Risk metrics
    portfolio_beta = Column(Float, nullable=True)
    portfolio_volatility = Column(Float, nullable=True)
    var_95 = Column(Float, nullable=True)  # Value at Risk 95%
    
    # Trading activity since last snapshot
    trades_count = Column(Integer, default=0, nullable=False)
    turnover_rate = Column(Float, nullable=True)
    
    # Relationships
    account = relationship("Account", back_populates="snapshots")
    
    def __repr__(self) -> str:
        return (
            f"<PortfolioSnapshot(account_id={self.account_id}, "
            f"value={self.total_value}, date={self.created_at})>"
        )
    
    @classmethod
    def create_from_account(
        cls, 
        account, 
        market_prices: dict[str, float],
        snapshot_type: str = "daily"
    ) -> "PortfolioSnapshot":
        """Create a snapshot from current account state."""
        # Calculate holdings value and breakdown
        holdings_breakdown = {}
        invested_value = 0.0
        
        for symbol, quantity in account.holdings.items():
            price = market_prices.get(symbol, 0.0)
            value = quantity * price
            invested_value += value
            
            holdings_breakdown[symbol] = {
                "quantity": quantity,
                "price": price,
                "value": value,
                "weight": 0.0  # Will be calculated below
            }
        
        total_value = account.balance + invested_value
        
        # Calculate weights
        if total_value > 0:
            for holding in holdings_breakdown.values():
                holding["weight"] = holding["value"] / total_value
        
        return cls(
            account_id=account.id,
            snapshot_type=snapshot_type,
            total_value=total_value,
            cash_balance=account.balance,
            invested_value=invested_value,
            holdings=holdings_breakdown
        )
    
    def calculate_sector_allocation(self, symbol_sectors: dict[str, str]) -> None:
        """Calculate and store sector allocation."""
        if not isinstance(self.holdings, dict):
            return
            
        sector_values = {}
        total_invested = 0.0
        
        for symbol, holding in self.holdings.items():
            sector = symbol_sectors.get(symbol, "Unknown")
            value = holding.get("value", 0.0)
            sector_values[sector] = sector_values.get(sector, 0.0) + value
            total_invested += value
        
        # Convert to percentages
        if total_invested > 0:
            sector_allocation = {
                sector: value / total_invested 
                for sector, value in sector_values.items()
            }
            self.sector_allocation = sector_allocation
    
    def get_top_holdings(self, n: int = 5) -> list[dict]:
        """Get top N holdings by value."""
        if not isinstance(self.holdings, dict):
            return []
        
        holdings_list = [
            {"symbol": symbol, **holding}
            for symbol, holding in self.holdings.items()
        ]
        
        return sorted(
            holdings_list, 
            key=lambda x: x.get("value", 0.0), 
            reverse=True
        )[:n]