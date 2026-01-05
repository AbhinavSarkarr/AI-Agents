"""Market data model for caching stock prices."""

from datetime import datetime, date
from sqlalchemy import Column, String, Float, Date, DateTime, JSON, Index

from .base import Base


class MarketData(Base):
    """Market data model for caching stock prices and market information."""
    
    __tablename__ = "market_data"
    
    # Stock identification
    symbol = Column(String(10), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    
    # Price data
    open_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=True)
    low_price = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    
    # Additional market data
    adjusted_close = Column(Float, nullable=True)
    dividend_amount = Column(Float, nullable=True)
    split_coefficient = Column(Float, nullable=True)
    
    # Market metadata
    data_source = Column(String(20), default="polygon", nullable=False)  # polygon, yahoo, etc.
    data_quality = Column(String(10), default="good", nullable=False)  # good, estimated, stale
    
    # Technical indicators (stored as JSON for flexibility)
    technical_indicators = Column(JSON, nullable=True)
    
    # Data freshness
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_real_time = Column(String(10), default="eod", nullable=False)  # eod, delayed, realtime
    
    # Composite indexes for efficient querying
    __table_args__ = (
        Index('idx_symbol_date', 'symbol', 'date'),
        Index('idx_date_source', 'date', 'data_source'),
    )
    
    def __repr__(self) -> str:
        return (
            f"<MarketData(symbol='{self.symbol}', date={self.date}, "
            f"close={self.close_price}, source='{self.data_source}')>"
        )
    
    @classmethod
    def create_eod_record(
        cls, 
        symbol: str, 
        date: date, 
        close_price: float,
        open_price: float = None,
        high_price: float = None,
        low_price: float = None,
        volume: float = None
    ) -> "MarketData":
        """Create an end-of-day market data record."""
        return cls(
            symbol=symbol,
            date=date,
            open_price=open_price,
            close_price=close_price,
            high_price=high_price,
            low_price=low_price,
            volume=volume,
            is_real_time="eod"
        )
    
    def is_stale(self, max_age_hours: int = 24) -> bool:
        """Check if the data is stale based on fetch time."""
        if not self.fetched_at:
            return True
        age = datetime.utcnow() - self.fetched_at
        return age.total_seconds() > (max_age_hours * 3600)
    
    def update_technical_indicators(self, indicators: dict) -> None:
        """Update technical indicators."""
        if not isinstance(self.technical_indicators, dict):
            self.technical_indicators = {}
        self.technical_indicators.update(indicators)