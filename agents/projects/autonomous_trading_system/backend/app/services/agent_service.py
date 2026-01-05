"""Agent service for managing AI trading agents."""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from .account_service import AccountService
from .market_service import MarketService
from .trading_service import TradingService
from ..models.account import Account
from ..models.strategy import Strategy
from ..models.agent_log import AgentLog, LogType
from ..core.config import settings


class TradingAgent:
    """Individual trading agent for an account."""
    
    def __init__(self, account_name: str, strategy_description: str):
        self.account_name = account_name
        self.strategy_description = strategy_description
        self.is_active = False
        self.do_trade = True  # Alternates between trade and rebalance
        
    async def execute_trading_cycle(self, db: Session):
        """Execute one trading cycle."""
        if not self.is_active:
            return
            
        trading_service = TradingService(db)
        market_service = MarketService(db)
        account_service = AccountService(db)
        
        try:
            account = account_service.get_account_by_name(self.account_name)
            if not account:
                return
                
            # Log start of trading cycle
            log = AgentLog(
                account_id=account.id,
                log_type=LogType.TRACE,
                message=f"Starting {'trading' if self.do_trade else 'rebalancing'} cycle"
            )
            db.add(log)
            db.commit()
            
            if self.do_trade:
                # Simulate finding new opportunities
                await self._execute_trades(account, trading_service, market_service, db)
            else:
                # Simulate rebalancing
                await self._rebalance_portfolio(account, trading_service, market_service, db)
            
            # Toggle between trade and rebalance
            self.do_trade = not self.do_trade
            
        except Exception as e:
            error_log = AgentLog.create_error_log(
                account_id=account.id if account else 0,
                message=f"Trading cycle error: {str(e)}",
                error_code="AGENT_CYCLE_ERROR"
            )
            db.add(error_log)
            db.commit()
    
    async def _execute_trades(self, account: Account, trading_service: TradingService, 
                            market_service: MarketService, db: Session):
        """Execute new trades based on strategy."""
        # Simulate agent decision making
        symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "SPY", "QQQ", "BTC"]
        
        # Decide whether to buy or sell
        action = random.choice(["buy", "sell", "hold"])
        
        if action == "hold":
            log = AgentLog(
                account_id=account.id,
                log_type=LogType.DECISION,
                message="Decided to hold current positions"
            )
            db.add(log)
            db.commit()
            return
        
        symbol = random.choice(symbols)
        
        if action == "buy":
            # Check if we have enough cash
            if account.balance > 100:
                max_shares = int(account.balance / 100)  # Rough estimate
                quantity = random.randint(1, min(10, max_shares))
                
                rationale = f"Based on {self.strategy_description}, identified opportunity in {symbol}"
                
                try:
                    result = trading_service.execute_buy_order(
                        account.name, symbol, quantity, rationale
                    )
                    
                    log = AgentLog(
                        account_id=account.id,
                        log_type=LogType.EXECUTION,
                        message=f"Successfully bought {quantity} shares of {symbol}"
                    )
                    db.add(log)
                    db.commit()
                    
                except Exception as e:
                    # Log failed attempt
                    log = AgentLog(
                        account_id=account.id,
                        log_type=LogType.ERROR,
                        message=f"Failed to buy {symbol}: {str(e)}"
                    )
                    db.add(log)
                    db.commit()
        
        elif action == "sell" and account.holdings:
            # Pick a random holding to sell
            holdings_list = list(account.holdings.keys())
            if holdings_list:
                symbol = random.choice(holdings_list)
                current_quantity = account.holdings[symbol]
                quantity = random.randint(1, min(current_quantity, 5))
                
                rationale = f"Taking profits or rebalancing based on {self.strategy_description}"
                
                try:
                    result = trading_service.execute_sell_order(
                        account.name, symbol, quantity, rationale
                    )
                    
                    log = AgentLog(
                        account_id=account.id,
                        log_type=LogType.EXECUTION,
                        message=f"Successfully sold {quantity} shares of {symbol}"
                    )
                    db.add(log)
                    db.commit()
                    
                except Exception as e:
                    # Log failed attempt
                    log = AgentLog(
                        account_id=account.id,
                        log_type=LogType.ERROR,
                        message=f"Failed to sell {symbol}: {str(e)}"
                    )
                    db.add(log)
                    db.commit()
    
    async def _rebalance_portfolio(self, account: Account, trading_service: TradingService,
                                  market_service: MarketService, db: Session):
        """Rebalance existing portfolio."""
        log = AgentLog(
            account_id=account.id,
            log_type=LogType.DECISION,
            message="Analyzing portfolio for rebalancing opportunities"
        )
        db.add(log)
        
        # Simple rebalancing logic - could be made more sophisticated
        if len(account.holdings) > 5:
            # Too many positions, sell some
            symbol = random.choice(list(account.holdings.keys()))
            quantity = 1
            
            try:
                trading_service.execute_sell_order(
                    account.name, symbol, quantity,
                    "Rebalancing: Reducing number of positions"
                )
            except:
                pass
        
        db.commit()


class AgentService:
    """Service for managing all trading agents."""
    
    def __init__(self, db: Session):
        self.db = db
        self.agents: Dict[str, TradingAgent] = {}
        self.trading_task = None
        self.is_running = False
        
        # Initialize agents for each account
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize trading agents for all accounts."""
        # Define strategies for each trader
        strategies = {
            "warren": "Value investing - seeking undervalued quality companies for long-term growth",
            "george": "Macro trading - making bold contrarian bets based on economic events", 
            "ray": "Systematic approach - diversified portfolio with risk parity principles",
            "cathie": "Innovation focus - aggressive positions in disruptive technology and crypto"
        }
        
        for name, strategy in strategies.items():
            self.agents[name] = TradingAgent(name, strategy)
    
    async def start_all_agents(self):
        """Start all trading agents."""
        if self.is_running:
            return {"status": "already_running", "message": "Trading agents are already running"}
        
        self.is_running = True
        for agent in self.agents.values():
            agent.is_active = True
        
        # Start the trading loop
        self.trading_task = asyncio.create_task(self._trading_loop())
        
        return {"status": "started", "message": "All trading agents started"}
    
    async def stop_all_agents(self):
        """Stop all trading agents."""
        self.is_running = False
        for agent in self.agents.values():
            agent.is_active = False
        
        if self.trading_task:
            self.trading_task.cancel()
            
        return {"status": "stopped", "message": "All trading agents stopped"}
    
    async def start_agent(self, account_name: str):
        """Start a specific trading agent."""
        if account_name not in self.agents:
            return {"status": "error", "message": f"Agent {account_name} not found"}
        
        self.agents[account_name].is_active = True
        
        # Start the trading loop if not already running
        if not self.is_running:
            self.is_running = True
            self.trading_task = asyncio.create_task(self._trading_loop())
        
        return {"status": "started", "message": f"Agent {account_name} started"}
    
    async def stop_agent(self, account_name: str):
        """Stop a specific trading agent."""
        if account_name not in self.agents:
            return {"status": "error", "message": f"Agent {account_name} not found"}
        
        self.agents[account_name].is_active = False
        
        # Check if all agents are stopped
        if not any(agent.is_active for agent in self.agents.values()):
            self.is_running = False
            if self.trading_task:
                self.trading_task.cancel()
        
        return {"status": "stopped", "message": f"Agent {account_name} stopped"}
    
    def get_agents_status(self) -> Dict:
        """Get status of all agents."""
        return {
            "is_running": self.is_running,
            "agents": {
                name: {
                    "is_active": agent.is_active,
                    "mode": "trading" if agent.do_trade else "rebalancing",
                    "strategy": agent.strategy_description
                }
                for name, agent in self.agents.items()
            }
        }
    
    async def _trading_loop(self):
        """Main trading loop that runs continuously."""
        while self.is_running:
            try:
                # Check if market is open (optional)
                market_service = MarketService(self.db)
                
                if not settings.run_even_when_market_is_closed and not market_service.is_market_open():
                    await asyncio.sleep(60)  # Check every minute when market is closed
                    continue
                
                # Execute trading cycle for each active agent
                for agent in self.agents.values():
                    if agent.is_active:
                        await agent.execute_trading_cycle(self.db)
                        await asyncio.sleep(2)  # Small delay between agents
                
                # Wait before next cycle (configurable, default 60 seconds for demo)
                await asyncio.sleep(60)  # Run every minute for demo purposes
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Trading loop error: {e}")
                await asyncio.sleep(10)  # Wait before retrying