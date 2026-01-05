"""Strategy model for agent trading strategies."""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Text, Boolean, Float, JSON, Enum as SQLEnum

from .base import Base


class StrategyType(str, Enum):
    """Strategy type enumeration."""
    VALUE = "value"
    GROWTH = "growth"
    MOMENTUM = "momentum"
    CONTRARIAN = "contrarian"
    SYSTEMATIC = "systematic"
    INNOVATION = "innovation"
    CRYPTO = "crypto"
    MACRO = "macro"


class RiskTolerance(str, Enum):
    """Risk tolerance enumeration."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    SPECULATIVE = "speculative"


class Strategy(Base):
    """Strategy model for defining agent trading strategies."""
    
    __tablename__ = "strategies"
    
    # Basic strategy info
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(150), nullable=True)
    description = Column(Text, nullable=False)
    
    # Strategy classification
    strategy_type = Column(SQLEnum(StrategyType), nullable=False)
    risk_tolerance = Column(SQLEnum(RiskTolerance), nullable=False)
    
    # Strategy parameters (stored as JSON for flexibility)
    parameters = Column(JSON, default=dict, nullable=False)
    
    # Position sizing rules
    max_position_size = Column(Float, default=0.2, nullable=False)  # Max % of portfolio per position
    max_portfolio_allocation = Column(Float, default=0.8, nullable=False)  # Max % invested
    stop_loss_percentage = Column(Float, nullable=True)
    take_profit_percentage = Column(Float, nullable=True)
    
    # Rebalancing rules
    rebalance_frequency_days = Column(Float, default=7, nullable=False)
    drift_threshold = Column(Float, default=0.05, nullable=False)  # 5% drift triggers rebalance
    
    # Trading constraints
    min_trade_size = Column(Float, default=100.0, nullable=False)
    max_trades_per_day = Column(Float, default=10, nullable=False)
    allowed_sectors = Column(JSON, nullable=True)  # List of allowed sectors
    prohibited_symbols = Column(JSON, nullable=True)  # List of prohibited symbols
    
    # Performance targets
    target_annual_return = Column(Float, nullable=True)
    target_sharpe_ratio = Column(Float, nullable=True)
    max_drawdown_limit = Column(Float, nullable=True)
    
    # Strategy status
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(String(10), default="1.0", nullable=False)
    
    def __repr__(self) -> str:
        return (
            f"<Strategy(name='{self.name}', type={self.strategy_type.value}, "
            f"risk={self.risk_tolerance.value})>"
        )
    
    def get_parameter(self, key: str, default=None):
        """Get a strategy parameter."""
        if not isinstance(self.parameters, dict):
            return default
        return self.parameters.get(key, default)
    
    def set_parameter(self, key: str, value) -> None:
        """Set a strategy parameter."""
        if not isinstance(self.parameters, dict):
            self.parameters = {}
        self.parameters[key] = value
    
    def is_symbol_allowed(self, symbol: str) -> bool:
        """Check if a symbol is allowed for this strategy."""
        if not self.prohibited_symbols:
            return True
        return symbol not in self.prohibited_symbols
    
    def calculate_position_size(self, portfolio_value: float, conviction: float = 1.0) -> float:
        """Calculate position size based on portfolio value and conviction."""
        max_size = portfolio_value * self.max_position_size
        return max_size * min(conviction, 1.0)
    
    @classmethod
    def create_warren_strategy(cls) -> "Strategy":
        """Create Warren Buffett inspired value strategy."""
        return cls(
            name="warren_patience",
            display_name="Warren (Patience) - Value Investor",
            description=(
                "Value-oriented investor who prioritizes long-term wealth creation. "
                "Identifies high-quality companies trading below intrinsic value."
            ),
            strategy_type=StrategyType.VALUE,
            risk_tolerance=RiskTolerance.CONSERVATIVE,
            max_position_size=0.25,
            max_portfolio_allocation=0.9,
            rebalance_frequency_days=30,
            parameters={
                "min_pe_ratio": 0.0,
                "max_pe_ratio": 20.0,
                "min_roe": 0.15,
                "min_market_cap": 1_000_000_000,
                "hold_period_days": 365
            }
        )
    
    @classmethod
    def create_george_strategy(cls) -> "Strategy":
        """Create George Soros inspired macro strategy."""
        return cls(
            name="george_bold",
            display_name="George (Bold) - Macro Trader",
            description=(
                "Aggressive macro trader who seeks significant market mispricings. "
                "Makes contrarian bets against prevailing sentiment."
            ),
            strategy_type=StrategyType.MACRO,
            risk_tolerance=RiskTolerance.AGGRESSIVE,
            max_position_size=0.3,
            max_portfolio_allocation=0.95,
            rebalance_frequency_days=3,
            parameters={
                "leverage_ratio": 1.5,
                "volatility_target": 0.25,
                "momentum_lookback": 30,
                "contrarian_threshold": 0.1
            }
        )