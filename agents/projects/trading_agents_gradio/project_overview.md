# Complete Autonomous Trading System Flow

## **Project Overview**
This is a **multi-agent autonomous stock trading simulation** featuring 4 AI traders, each with distinct personalities and strategies, that operate continuously to manage their portfolios using real market data, web research, and autonomous decision-making.

## **The Four Trading Agents**

**Warren** ("Patience") - Value investor inspired by Warren Buffett
- Strategy: Long-term value investing, fundamental analysis
- Behavior: Patient, holds through volatility, seeks undervalued quality companies

**George** ("Bold") - Macro trader inspired by George Soros  
- Strategy: Aggressive macro trading, contrarian bets
- Behavior: Bold moves based on economic/geopolitical events

**Ray** ("Systematic") - Systematic investor inspired by Ray Dalio
- Strategy: Risk parity, diversified across asset classes
- Behavior: Principles-based, macroeconomic indicators-driven

**Cathie** ("Crypto") - Innovation investor inspired by Cathie Wood
- Strategy: Disruptive innovation focus, especially crypto ETFs
- Behavior: High-risk, high-reward tech/crypto investments

## **Complete System Architecture**

### **1. Trading Floor Engine (`trading_floor.py`)**
```
Main Loop:
┌─ Every N minutes (default: 60) ─┐
│  Check if market is open        │
│  Run all 4 traders in parallel  │
│  Sleep until next cycle         │
└─ Repeat forever               ─┘
```

### **2. Individual Trader Lifecycle (`traders.py`)**

**Each trader alternates between two modes:**
- **Trading Mode**: Find new opportunities, execute trades
- **Rebalancing Mode**: Review existing portfolio, adjust positions

**Per-run flow:**
1. **Setup MCP Servers** (Accounts, Market Data, Push Notifications)
2. **Create Researcher Agent** (as a tool with web search + memory)
3. **Load Account & Strategy** from database
4. **Execute Trading Logic**:
   - Research opportunities using web search
   - Analyze market data via Polygon API
   - Make trading decisions
   - Execute buy/sell orders
   - Send push notifications
   - Log all activity
5. **Cleanup & Switch Mode**

### **3. MCP (Model Context Protocol) Architecture**

**Trader MCP Servers:**
- **Accounts Server** (`accounts_server.py`): Portfolio management tools
  - `buy_shares()`, `sell_shares()`, `get_balance()`, `get_holdings()`
- **Market Server** (`market_server.py`): Stock price data
  - `lookup_share_price()` using Polygon API
- **Push Server** (`push_server.py`): Notifications
  - `push()` sends updates via Pushover

**Researcher MCP Servers:**
- **Fetch Server**: Web scraping capabilities
- **Serper Server**: Google search API
- **Memory Server**: Persistent knowledge graph per agent

### **4. Data Flow Architecture**

```
┌─ Polygon API ─┐    ┌─ Web Research ─┐    ┌─ Account DB ─┐
│ Stock Prices  │    │ News/Analysis  │    │ Balances    │
│ EOD/Realtime  │───▶│ Search Results │◀──▶│ Holdings    │
└───────────────┘    └────────────────┘    │ Transactions│
        │                     │             └─────────────┘
        ▼                     ▼                     ▲
┌────────────────────────────────────────────────────┐
│              TRADER AGENT                          │
│ ┌─ Researcher ─┐  ┌─ Decision ─┐  ┌─ Execution ─┐ │
│ │ Web Search   │──│ Making     │──│ Trading     │ │
│ │ News Analysis│  │ AI Logic   │  │ Orders      │ │
│ │ Memory Recall│  └────────────┘  └─────────────┘ │
│ └──────────────┘                                  │
└────────────────────────────────────────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌─ Push Notifications ─┐ ┌─ Activity Logs ─┐ ┌─ Dashboard ─┐
│ Trade Summaries     │ │ Trace Data      │ │ Real-time UI│
│ Portfolio Health    │ │ Decision Steps  │ │ Charts/Data │
└─────────────────────┘ └─────────────────┘ └─────────────┘
```

### **5. Decision Making Process**

**Each trader follows this autonomous decision loop:**

1. **Research Phase**:
   - Search web for market news, company updates
   - Query memory for past insights about stocks
   - Analyze current portfolio performance

2. **Analysis Phase**:
   - Get current stock prices via Polygon API
   - Apply their unique investment strategy
   - Consider macroeconomic factors
   - Review existing positions

3. **Decision Phase**:
   - Determine which stocks to buy/sell
   - Calculate position sizes based on strategy
   - Generate rationale for each trade

4. **Execution Phase**:
   - Execute trades via account management tools
   - Log all transactions to database
   - Send push notifications about activity
   - Update portfolio valuations

5. **Memory Phase**:
   - Store new insights in persistent memory
   - Record market observations
   - Update strategy notes if needed

### **6. Real-Time Monitoring**

**Dashboard UI (`app.py`)**:
- **Live portfolio values** (updates every 3 seconds)
- **Holdings tables** showing current positions
- **Transaction history** with rationales
- **Activity logs** showing agent thinking process
- **Performance charts** tracking P&L over time

**Tracing System (`tracers.py`)**:
- Captures detailed execution traces
- Records agent decisions and tool usage
- Stores activity logs for UI display
- Enables debugging and performance analysis

## **Polygon API Integration**

### **Configuration & Plan Types**
The system checks for two environment variables:
- `POLYGON_API_KEY`: Your API key
- `POLYGON_PLAN`: Can be "free" (default), "paid", or "realtime"

### **Free Plan Limitations & Fallbacks**
On the **free plan**, the system:
- Uses **End-of-Day (EOD) data only** via `get_share_price_polygon_eod()`
- Fetches previous day's closing prices using `get_grouped_daily_aggs()`
- **Caches data** to avoid hitting rate limits (`@lru_cache`)
- **Falls back to random prices** if API fails

### **API Usage Breakdown**

**Free Plan (`market.py:25-48`)**:
1. **Market Status Check**: `get_market_status()` - checks if market is open
2. **Bulk EOD Data**: `get_grouped_daily_aggs(last_close_date)` - fetches all stock prices for previous trading day
3. **Data Caching**: Results cached in local database to minimize API calls
4. **Single Stock Lookup**: Returns cached EOD price for requested symbol

**Paid Plan (`market.py:51-54`)**:
- **Real-time Snapshots**: `get_snapshot_ticker()` - gets current/15-min delayed prices
- **Minute-level Data**: Access to intraday pricing

**Realtime Plan**:
- **Live Trade Data**: Direct access to latest trade prices
- **Full Market Tools**: Technical indicators, fundamentals, trends

## **Key Features**

1. **Fully Autonomous**: Runs 24/7 without human intervention
2. **Multi-Modal AI**: Each agent has unique personality and strategy
3. **Real Market Data**: Uses Polygon API for actual stock prices
4. **Web Research**: Agents search news and analyze market conditions
5. **Persistent Memory**: Agents remember past decisions and market insights
6. **Risk Management**: Built-in position sizing and portfolio constraints
7. **Real-Time Monitoring**: Live dashboard with detailed activity tracking
8. **Push Notifications**: Mobile alerts for significant trading activity

## **What the Agents Actually Do**

The agents operate like **autonomous hedge fund managers**:
- **Research** market opportunities continuously
- **Make investment decisions** based on their strategies
- **Execute real trades** (simulated with $10K starting capital each)
- **Manage risk** and rebalance portfolios
- **Learn from experience** using persistent memory
- **Communicate findings** through notifications and logs

The system simulates a **real trading environment** where AI agents compete and collaborate, each following their distinct investment philosophies while adapting to changing market conditions.

## **Running the System**

### **Prerequisites**
Set up environment variables in `.env`:
- `POLYGON_API_KEY`: Your Polygon.io API key
- `POLYGON_PLAN`: "free", "paid", or "realtime"
- `SERPER_API_KEY`: For web search functionality
- `PUSHOVER_USER` & `PUSHOVER_TOKEN`: For push notifications (optional)

### **Optional Configuration**
- `RUN_EVERY_N_MINUTES=60`: How often traders run (default: 60 minutes)
- `RUN_EVEN_WHEN_MARKET_IS_CLOSED=False`: Run outside market hours (default: False)
- `USE_MANY_MODELS=False`: Use multiple AI models vs just GPT-4o-mini (default: False)

### **Start the System**

1. **Launch Dashboard** (in one terminal):
   ```bash
   uv run app.py
   ```
   Access at http://127.0.0.1:7860

2. **Start Trading Floor** (in another terminal):
   ```bash
   uv run trading_floor.py
   ```
   This runs the main trading loop

### **Reset Traders** (optional):
```bash
uv run reset.py
```
Resets all trader accounts to initial $10K balance and default strategies.

## **File Structure**

- `trading_floor.py`: Main execution engine and scheduler
- `traders.py`: Individual trader agent implementation
- `accounts.py`: Portfolio management and trading logic
- `accounts_server.py`: MCP server for account operations
- `market.py`: Polygon API integration and price fetching
- `market_server.py`: MCP server for market data
- `push_server.py`: MCP server for push notifications
- `app.py`: Gradio-based dashboard UI
- `templates.py`: Agent instructions and prompts
- `tracers.py`: Activity logging and tracing
- `database.py`: SQLite database operations
- `reset.py`: Reset traders to initial state
- `mcp_params.py`: MCP server configuration