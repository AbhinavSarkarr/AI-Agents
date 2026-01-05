"""
Configuration management for the trading system.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    polygon_api_key: Optional[str] = Field(default=None, env="POLYGON_API_KEY")
    polygon_plan: str = Field(default="free", env="POLYGON_PLAN")
    serper_api_key: Optional[str] = Field(default=None, env="SERPER_API_KEY")
    
    # Push Notifications
    pushover_user: Optional[str] = Field(default=None, env="PUSHOVER_USER")
    pushover_token: Optional[str] = Field(default=None, env="PUSHOVER_TOKEN")
    
    # AI Model Keys
    deepseek_api_key: Optional[str] = Field(default=None, env="DEEPSEEK_API_KEY")
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    grok_api_key: Optional[str] = Field(default=None, env="GROK_API_KEY")
    openrouter_api_key: Optional[str] = Field(default=None, env="OPENROUTER_API_KEY")
    
    # Trading Configuration
    run_every_n_minutes: int = Field(default=60, env="RUN_EVERY_N_MINUTES")
    run_even_when_market_is_closed: bool = Field(default=False, env="RUN_EVEN_WHEN_MARKET_IS_CLOSED")
    use_many_models: bool = Field(default=False, env="USE_MANY_MODELS")
    initial_balance: float = Field(default=10000.0, env="INITIAL_BALANCE")
    spread: float = Field(default=0.002, env="SPREAD")
    
    # Database
    database_url: str = Field(default="sqlite:///./data/trading_system.db", env="DATABASE_URL")
    
    # Security
    secret_key: str = Field(default="your-super-secret-key", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Model Configuration
    @property
    def is_paid_polygon(self) -> bool:
        return self.polygon_plan == "paid"
    
    @property
    def is_realtime_polygon(self) -> bool:
        return self.polygon_plan == "realtime"
    
    @property
    def model_names(self) -> List[str]:
        if self.use_many_models:
            return [
                "gpt-4.1-mini",
                "deepseek-chat", 
                "gemini-2.5-flash-preview-04-17",
                "grok-3-mini-beta",
            ]
        return ["gpt-4o-mini"] * 4
    
    @property
    def short_model_names(self) -> List[str]:
        if self.use_many_models:
            return ["GPT 4.1 Mini", "DeepSeek V3", "Gemini 2.5 Flash", "Grok 3 Mini"]
        return ["GPT 4o mini"] * 4
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables


# Global settings instance
settings = Settings()