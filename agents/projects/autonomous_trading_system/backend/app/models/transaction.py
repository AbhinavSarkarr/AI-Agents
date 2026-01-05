"""Transaction model for tracking trades."""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship

from .base import Base


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    BUY = "buy"
    SELL = "sell"


class TransactionStatus(str, Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(Base):
    """Transaction model for recording trades."""
    
    __tablename__ = "transactions"
    
    # Basic transaction info
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String(10), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)  # Positive for buy, negative for sell
    price = Column(Float, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.COMPLETED)
    
    # Trading context
    rationale = Column(Text, nullable=True)  # AI's reasoning for the trade
    strategy_context = Column(Text, nullable=True)  # Strategy being followed
    
    # Financial calculations
    total_value = Column(Float, nullable=False)  # quantity * price
    fees = Column(Float, default=0.0, nullable=False)
    net_value = Column(Float, nullable=False)  # total_value - fees
    
    # Market context at time of trade
    market_price = Column(Float, nullable=True)  # Actual market price (for spread calculation)
    spread_percentage = Column(Float, nullable=True)
    
    # Execution details
    execution_time = Column(Float, nullable=True)  # Time taken to execute in seconds
    error_message = Column(Text, nullable=True)  # If transaction failed
    
    # Relationships
    account = relationship("Account", back_populates="transactions")
    
    def __repr__(self) -> str:
        return (
            f"<Transaction(symbol='{self.symbol}', type={self.transaction_type.value}, "
            f"quantity={self.quantity}, price={self.price}, status={self.status.value})>"
        )
    
    @property
    def is_buy(self) -> bool:
        """Check if this is a buy transaction."""
        return self.transaction_type == TransactionType.BUY
    
    @property
    def is_sell(self) -> bool:
        """Check if this is a sell transaction."""
        return self.transaction_type == TransactionType.SELL
    
    def calculate_total_value(self) -> float:
        """Calculate total transaction value."""
        return abs(self.quantity) * self.price
    
    def calculate_net_value(self) -> float:
        """Calculate net transaction value after fees."""
        return self.calculate_total_value() - self.fees