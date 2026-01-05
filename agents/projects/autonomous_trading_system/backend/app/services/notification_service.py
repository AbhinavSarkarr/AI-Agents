"""Notification service for push notifications and alerts."""

import requests
from typing import Optional
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.agent_log import AgentLog, LogType


class NotificationService:
    """Service for handling notifications and alerts."""
    
    def __init__(self, db: Session):
        self.db = db
        self.pushover_url = "https://api.pushover.net/1/messages.json"
    
    def send_push_notification(self, message: str, priority: int = 0) -> bool:
        """
        Send a push notification via Pushover.
        
        Args:
            message: The message to send
            priority: Priority level (-2 to 2, default 0)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        # Always log the notification
        print(f"Push Notification: {message}")
        
        # If no Pushover credentials, just log and return
        if not settings.pushover_user or not settings.pushover_token:
            return True
        
        try:
            payload = {
                "user": settings.pushover_user,
                "token": settings.pushover_token,
                "message": message,
                "priority": priority
            }
            
            response = requests.post(self.pushover_url, data=payload, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                print(f"Pushover API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Failed to send push notification: {e}")
            return False
    
    def send_trading_alert(self, account_name: str, symbol: str, action: str, quantity: int, price: float) -> None:
        """Send a trading-specific alert."""
        message = f"{account_name}: {action.upper()} {quantity} {symbol} @ ${price:.2f}"
        self.send_push_notification(message)
    
    def send_portfolio_update(self, account_name: str, portfolio_value: float, profit_loss: float) -> None:
        """Send a portfolio performance update."""
        pl_sign = "+" if profit_loss >= 0 else ""
        message = f"{account_name}: Portfolio ${portfolio_value:,.0f} ({pl_sign}${profit_loss:,.0f})"
        priority = 1 if abs(profit_loss) > 1000 else 0  # High priority for large changes
        self.send_push_notification(message, priority)
    
    def send_error_alert(self, account_name: str, error_message: str) -> None:
        """Send an error alert."""
        message = f"ERROR - {account_name}: {error_message}"
        self.send_push_notification(message, priority=1)
    
    def send_system_alert(self, message: str, priority: int = 0) -> None:
        """Send a system-level alert."""
        system_message = f"SYSTEM: {message}"
        self.send_push_notification(system_message, priority)