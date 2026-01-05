"""Account management service."""

from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from ..models.account import Account
from ..models.transaction import Transaction, TransactionType, TransactionStatus
from ..models.portfolio_snapshot import PortfolioSnapshot
from ..models.agent_log import AgentLog
from ..core.config import settings


class AccountService:
    """Service for managing trading accounts."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_account_by_name(self, name: str) -> Optional[Account]:
        """Get account by name."""
        return self.db.query(Account).filter(Account.name == name.lower()).first()
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts."""
        return self.db.query(Account).filter(Account.is_active == True).all()
    
    def create_account(
        self, 
        name: str, 
        display_name: str = None,
        initial_balance: float = None
    ) -> Account:
        """Create a new trading account."""
        if self.get_account_by_name(name):
            raise ValueError(f"Account with name '{name}' already exists")
        
        account = Account(
            name=name.lower(),
            display_name=display_name or name.title(),
            balance=initial_balance or settings.initial_balance,
            holdings={},
            portfolio_value_history=[]
        )
        
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def reset_account(self, account_id: int, strategy_description: str = None) -> Account:
        """Reset account to initial state."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        # Delete all transactions and logs
        self.db.query(Transaction).filter(Transaction.account_id == account_id).delete()
        self.db.query(AgentLog).filter(AgentLog.account_id == account_id).delete()
        self.db.query(PortfolioSnapshot).filter(PortfolioSnapshot.account_id == account_id).delete()
        
        # Reset account state
        account.balance = settings.initial_balance
        account.holdings = {}
        account.portfolio_value_history = []
        account.total_portfolio_value = settings.initial_balance
        account.total_profit_loss = 0.0
        account.win_rate = 0.0
        account.sharpe_ratio = None
        account.max_drawdown = None
        
        # Log the reset
        reset_log = AgentLog.create_trace_log(
            account_id=account.id,
            message=f"Account reset with strategy: {strategy_description or 'No strategy specified'}"
        )
        self.db.add(reset_log)
        
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def buy_shares(
        self, 
        account_id: int, 
        symbol: str, 
        quantity: int, 
        price: float,
        rationale: str = None
    ) -> float:
        """Execute a buy order."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        # Apply spread
        buy_price = price * (1 + settings.spread)
        total_cost = buy_price * quantity
        
        # Check sufficient funds
        if total_cost > account.balance:
            raise ValueError("Insufficient funds to buy shares")
        
        if price <= 0:
            raise ValueError(f"Invalid price for symbol {symbol}")
        
        # Create transaction record
        transaction = Transaction(
            account_id=account.id,
            symbol=symbol.upper(),
            quantity=quantity,
            price=buy_price,
            transaction_type=TransactionType.BUY,
            status=TransactionStatus.COMPLETED,
            rationale=rationale,
            total_value=total_cost,
            net_value=total_cost,
            market_price=price,
            spread_percentage=settings.spread
        )
        
        # Update account
        account.balance -= total_cost
        account.add_holding(symbol.upper(), quantity)
        
        # Save transaction
        self.db.add(transaction)
        self.db.commit()
        
        # Log the transaction
        buy_log = AgentLog.create_trace_log(
            account_id=account.id,
            message=f"Bought {quantity} shares of {symbol.upper()} at ${buy_price:.2f}",
            details={"symbol": symbol.upper(), "quantity": quantity, "price": buy_price, "total": total_cost}
        )
        self.db.add(buy_log)
        self.db.commit()
        
        return total_cost
    
    def sell_shares(
        self, 
        account_id: int, 
        symbol: str, 
        quantity: int, 
        price: float,
        rationale: str = None
    ) -> float:
        """Execute a sell order."""
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        
        symbol = symbol.upper()
        
        # Check sufficient holdings
        if not account.remove_holding(symbol, quantity):
            current_holdings = account.holdings.get(symbol, 0)
            raise ValueError(f"Cannot sell {quantity} shares of {symbol}. Only have {current_holdings} shares.")
        
        # Apply spread
        sell_price = price * (1 - settings.spread)
        total_proceeds = sell_price * quantity
        
        # Create transaction record
        transaction = Transaction(
            account_id=account.id,
            symbol=symbol,
            quantity=-quantity,  # Negative for sell
            price=sell_price,
            transaction_type=TransactionType.SELL,
            status=TransactionStatus.COMPLETED,
            rationale=rationale,
            total_value=total_proceeds,
            net_value=total_proceeds,
            market_price=price,
            spread_percentage=settings.spread
        )
        
        # Update account
        account.balance += total_proceeds
        
        # Save transaction
        self.db.add(transaction)
        self.db.commit()
        
        # Log the transaction
        sell_log = AgentLog.create_trace_log(
            account_id=account.id,
            message=f"Sold {quantity} shares of {symbol} at ${sell_price:.2f}",
            details={"symbol": symbol, "quantity": quantity, "price": sell_price, "total": total_proceeds}
        )
        self.db.add(sell_log)
        self.db.commit()
        
        return total_proceeds
    
    def calculate_portfolio_value(self, account: Account, market_prices: Dict[str, float]) -> float:
        """Calculate current portfolio value."""
        return account.calculate_portfolio_value(market_prices)
    
    def update_portfolio_metrics(self, account: Account, current_value: float) -> None:
        """Update portfolio performance metrics."""
        account.update_portfolio_value(current_value)
        
        # Calculate profit/loss
        initial_value = settings.initial_balance
        account.total_profit_loss = current_value - initial_value
        
        # Calculate win rate from transactions
        transactions = self.db.query(Transaction).filter(
            Transaction.account_id == account.id,
            Transaction.transaction_type == TransactionType.SELL
        ).all()
        
        if transactions:
            # Simple win rate calculation based on profitable sells
            # This is a simplified version - in practice, you'd match buy/sell pairs
            profitable_trades = sum(1 for t in transactions if t.price > 0)  # Placeholder logic
            account.win_rate = profitable_trades / len(transactions) if transactions else 0.0
        
        self.db.commit()
    
    def create_portfolio_snapshot(
        self, 
        account: Account, 
        market_prices: Dict[str, float],
        snapshot_type: str = "daily"
    ) -> PortfolioSnapshot:
        """Create a portfolio snapshot."""
        snapshot = PortfolioSnapshot.create_from_account(account, market_prices, snapshot_type)
        snapshot.account_id = account.id
        
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return snapshot
    
    def get_account_transactions(
        self, 
        account_id: int, 
        limit: int = 50
    ) -> List[Transaction]:
        """Get recent transactions for an account."""
        return (
            self.db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .order_by(Transaction.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_account_logs(
        self, 
        account_id: int, 
        limit: int = 100
    ) -> List[AgentLog]:
        """Get recent logs for an account."""
        return (
            self.db.query(AgentLog)
            .filter(AgentLog.account_id == account_id)
            .order_by(AgentLog.created_at.desc())
            .limit(limit)
            .all()
        )