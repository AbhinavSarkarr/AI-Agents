"""Trading orchestration service."""

from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from .account_service import AccountService  
from .market_service import MarketService
from .notification_service import NotificationService
from ..models.account import Account
from ..models.agent_log import AgentLog, LogType


class TradingService:
    """Service for orchestrating trading operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.account_service = AccountService(db)
        self.market_service = MarketService(db)
        self.notification_service = NotificationService(db)
    
    def execute_buy_order(
        self, 
        account_name: str, 
        symbol: str, 
        quantity: int, 
        rationale: str = None
    ) -> Dict:
        """Execute a buy order for an account."""
        # Get account
        account = self.account_service.get_account_by_name(account_name)
        if not account:
            raise ValueError(f"Account '{account_name}' not found")
        
        # Get current market price
        market_price = self.market_service.get_share_price(symbol)
        if market_price <= 0:
            raise ValueError(f"Invalid market price for {symbol}: {market_price}")
        
        # Log the decision
        decision_log = AgentLog(
            account_id=account.id,
            log_type=LogType.DECISION,
            message=f"Decided to buy {quantity} shares of {symbol} at market price ${market_price:.2f}",
            details={
                "action": "buy",
                "symbol": symbol,
                "quantity": quantity,
                "market_price": market_price,
                "rationale": rationale
            }
        )
        self.db.add(decision_log)
        
        try:
            # Execute the trade
            total_cost = self.account_service.buy_shares(
                account.id, symbol, quantity, market_price, rationale
            )
            
            # Update portfolio metrics
            market_prices = self.market_service.get_multiple_prices(list(account.holdings.keys()))
            current_value = self.account_service.calculate_portfolio_value(account, market_prices)
            self.account_service.update_portfolio_metrics(account, current_value)
            
            # Send notification
            message = f"{account.display_name} bought {quantity} shares of {symbol} for ${total_cost:.2f}"
            self.notification_service.send_push_notification(message)
            
            # Log success
            success_log = AgentLog(
                account_id=account.id,
                log_type=LogType.EXECUTION,
                message=f"Successfully bought {quantity} shares of {symbol}",
                details={
                    "action": "buy",
                    "symbol": symbol,
                    "quantity": quantity,
                    "total_cost": total_cost,
                    "new_balance": account.balance,
                    "new_portfolio_value": current_value
                }
            )
            self.db.add(success_log)
            self.db.commit()
            
            return {
                "success": True,
                "symbol": symbol,
                "quantity": quantity,
                "total_cost": total_cost,
                "new_balance": account.balance,
                "portfolio_value": current_value
            }
            
        except Exception as e:
            # Log error
            error_log = AgentLog.create_error_log(
                account_id=account.id,
                message=f"Failed to buy {quantity} shares of {symbol}: {str(e)}",
                error_code="TRADE_EXECUTION_ERROR"
            )
            self.db.add(error_log)
            self.db.commit()
            raise
    
    def execute_sell_order(
        self, 
        account_name: str, 
        symbol: str, 
        quantity: int, 
        rationale: str = None
    ) -> Dict:
        """Execute a sell order for an account."""
        # Get account
        account = self.account_service.get_account_by_name(account_name)
        if not account:
            raise ValueError(f"Account '{account_name}' not found")
        
        # Get current market price
        market_price = self.market_service.get_share_price(symbol)
        if market_price <= 0:
            raise ValueError(f"Invalid market price for {symbol}: {market_price}")
        
        # Log the decision
        decision_log = AgentLog(
            account_id=account.id,
            log_type=LogType.DECISION,
            message=f"Decided to sell {quantity} shares of {symbol} at market price ${market_price:.2f}",
            details={
                "action": "sell",
                "symbol": symbol,
                "quantity": quantity,
                "market_price": market_price,
                "rationale": rationale
            }
        )
        self.db.add(decision_log)
        
        try:
            # Execute the trade
            total_proceeds = self.account_service.sell_shares(
                account.id, symbol, quantity, market_price, rationale
            )
            
            # Update portfolio metrics
            remaining_symbols = [s for s in account.holdings.keys() if account.holdings[s] > 0]
            market_prices = self.market_service.get_multiple_prices(remaining_symbols) if remaining_symbols else {}
            current_value = self.account_service.calculate_portfolio_value(account, market_prices)
            self.account_service.update_portfolio_metrics(account, current_value)
            
            # Send notification
            message = f"{account.display_name} sold {quantity} shares of {symbol} for ${total_proceeds:.2f}"
            self.notification_service.send_push_notification(message)
            
            # Log success
            success_log = AgentLog(
                account_id=account.id,
                log_type=LogType.EXECUTION,
                message=f"Successfully sold {quantity} shares of {symbol}",
                details={
                    "action": "sell",
                    "symbol": symbol,
                    "quantity": quantity,
                    "total_proceeds": total_proceeds,
                    "new_balance": account.balance,
                    "new_portfolio_value": current_value
                }
            )
            self.db.add(success_log)
            self.db.commit()
            
            return {
                "success": True,
                "symbol": symbol,
                "quantity": quantity,
                "total_proceeds": total_proceeds,
                "new_balance": account.balance,
                "portfolio_value": current_value
            }
            
        except Exception as e:
            # Log error
            error_log = AgentLog.create_error_log(
                account_id=account.id,
                message=f"Failed to sell {quantity} shares of {symbol}: {str(e)}",
                error_code="TRADE_EXECUTION_ERROR"
            )
            self.db.add(error_log)
            self.db.commit()
            raise
    
    def get_trading_summary(self, account_name: str) -> Dict:
        """Get trading summary for an account."""
        account = self.account_service.get_account_by_name(account_name)
        if not account:
            raise ValueError(f"Account '{account_name}' not found")
        
        # Get current market prices for holdings
        symbols = list(account.holdings.keys()) if account.holdings else []
        market_prices = self.market_service.get_multiple_prices(symbols)
        
        # Calculate current portfolio value
        current_value = self.account_service.calculate_portfolio_value(account, market_prices)
        
        # Get recent transactions
        recent_transactions = self.account_service.get_account_transactions(account.id, 10)
        
        return {
            "account_name": account.name,
            "display_name": account.display_name,
            "cash_balance": account.balance,
            "holdings": account.holdings,
            "portfolio_value": current_value,
            "profit_loss": account.total_profit_loss,
            "win_rate": account.win_rate,
            "recent_transactions": [
                {
                    "symbol": t.symbol,
                    "type": t.transaction_type.value,
                    "quantity": abs(t.quantity),
                    "price": t.price,
                    "timestamp": t.created_at.isoformat(),
                    "rationale": t.rationale
                }
                for t in recent_transactions
            ],
            "market_prices": market_prices,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def get_all_accounts_summary(self) -> List[Dict]:
        """Get summary for all active accounts."""
        accounts = self.account_service.get_all_accounts()
        summaries = []
        
        for account in accounts:
            try:
                summary = self.get_trading_summary(account.name)
                summaries.append(summary)
            except Exception as e:
                # Log error but continue with other accounts
                error_log = AgentLog.create_error_log(
                    account_id=account.id,
                    message=f"Failed to generate summary: {str(e)}",
                    error_code="SUMMARY_GENERATION_ERROR"
                )
                self.db.add(error_log)
        
        self.db.commit()
        return summaries