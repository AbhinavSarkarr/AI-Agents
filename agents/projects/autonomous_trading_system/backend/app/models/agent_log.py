"""Agent activity logging model."""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, Float,ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship

from .base import Base


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogType(str, Enum):
    """Log type enumeration for different agent activities."""
    TRACE = "trace"
    AGENT = "agent"
    FUNCTION = "function"
    GENERATION = "generation"
    RESPONSE = "response"
    ACCOUNT = "account"
    RESEARCH = "research"
    DECISION = "decision"
    EXECUTION = "execution"
    ERROR = "error"


class AgentLog(Base):
    """Agent activity log model."""
    
    __tablename__ = "agent_logs"
    
    # Basic log info
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    level = Column(SQLEnum(LogLevel), default=LogLevel.INFO, nullable=False)
    log_type = Column(SQLEnum(LogType), nullable=False)
    
    # Log content
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)  # Additional structured data
    
    # Context information
    trace_id = Column(String(100), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    function_name = Column(String(100), nullable=True)
    model_name = Column(String(50), nullable=True)
    
    # Performance metrics
    duration_ms = Column(Integer, nullable=True)  # Duration in milliseconds
    tokens_used = Column(Integer, nullable=True)  # For AI model calls
    cost_usd = Column(Float, nullable=True)  # Estimated cost
    
    # Error context (if applicable)
    error_code = Column(String(20), nullable=True)
    stack_trace = Column(Text, nullable=True)
    
    # Relationships
    account = relationship("Account", back_populates="logs")
    
    def __repr__(self) -> str:
        return (
            f"<AgentLog(account_id={self.account_id}, type={self.log_type.value}, "
            f"level={self.level.value}, message='{self.message[:50]}...')>"
        )
    
    @classmethod
    def create_trace_log(
        cls, 
        account_id: int, 
        message: str, 
        trace_id: str = None,
        details: dict = None
    ) -> "AgentLog":
        """Create a trace log entry."""
        return cls(
            account_id=account_id,
            level=LogLevel.INFO,
            log_type=LogType.TRACE,
            message=message,
            trace_id=trace_id,
            details=details
        )
    
    @classmethod
    def create_decision_log(
        cls, 
        account_id: int, 
        message: str, 
        decision_data: dict = None,
        trace_id: str = None
    ) -> "AgentLog":
        """Create a decision log entry."""
        return cls(
            account_id=account_id,
            level=LogLevel.INFO,
            log_type=LogType.DECISION,
            message=message,
            details=decision_data,
            trace_id=trace_id
        )
    
    @classmethod
    def create_error_log(
        cls, 
        account_id: int, 
        message: str, 
        error_code: str = None,
        stack_trace: str = None,
        trace_id: str = None
    ) -> "AgentLog":
        """Create an error log entry."""
        return cls(
            account_id=account_id,
            level=LogLevel.ERROR,
            log_type=LogType.ERROR,
            message=message,
            error_code=error_code,
            stack_trace=stack_trace,
            trace_id=trace_id
        )