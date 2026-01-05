# Agentic AI Ecosystem

A comprehensive multi-agent artificial intelligence platform featuring autonomous trading systems, specialized AI crews, and intelligent assistant frameworks built with cutting-edge LLM technologies.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Projects](#projects)
- [Frameworks](#frameworks)
- [Technologies](#technologies)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This repository serves as a comprehensive exploration and implementation of agentic AI systems, demonstrating various approaches to building intelligent, autonomous agents. The flagship component is a **Multi-Agent Autonomous Trading System** featuring four distinct AI traders, each embodying different investment philosophies and strategies.

The project showcases:
- **Autonomous Decision Making**: AI agents that independently analyze market conditions and execute trades
- **Multi-Agent Collaboration**: Systems where multiple specialized agents work together to achieve complex goals
- **Real-Time Market Integration**: Live stock market data processing and portfolio management
- **Modern Full-Stack Architecture**: Production-ready web applications with FastAPI backends and React frontends

---

## Key Features

### Autonomous Trading System
- **4 AI Traders with Distinct Strategies**:
  - **Warren** (Value Investor): Long-term fundamental analysis, seeks undervalued assets
  - **George** (Macro Trader): Contrarian approach, bold macro-economic plays
  - **Ray** (Systematic/Risk Parity): Diversified, risk-balanced portfolio management
  - **Cathie** (Innovation/Crypto): High-risk technology and cryptocurrency focus

- **Real-Time Portfolio Management**: Live tracking of positions, P&L, and market movements
- **MCP-Based Tool Architecture**: Extensible Model Context Protocol for agent capabilities
- **Persistent Memory System**: Agents learn from past decisions and market patterns
- **Push Notifications**: Real-time trading alerts via Pushover integration
- **Interactive Dashboards**: Both Gradio and React-based user interfaces

### Multi-Agent Frameworks
- **CrewAI Implementations**: Specialized crews for stock picking, financial research, engineering tasks, and code generation
- **Hierarchical Task Processing**: Agents with defined roles working collaboratively
- **Long-Term Memory Integration**: Entity tracking and knowledge graphs across sessions

### AI Assistant Capabilities
- **RAG-Enabled Chatbot**: Retrieval-Augmented Generation with vector database support
- **Multi-LLM Support**: Integration with OpenAI, Anthropic Claude, Google Gemini, Groq, and DeepSeek

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           AGENTIC AI ECOSYSTEM                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────┐    ┌──────────────────────┐                  │
│  │   Trading Agents     │    │    CrewAI Agents     │                  │
│  │  ┌────┐ ┌────┐       │    │  ┌─────────────────┐ │                  │
│  │  │War-│ │Geo-│       │    │  │  Stock Picker   │ │                  │
│  │  │ren │ │rge │       │    │  │  Debate Crew    │ │                  │
│  │  └────┘ └────┘       │    │  │  Financial Res. │ │                  │
│  │  ┌────┐ ┌────┐       │    │  │  Engineering    │ │                  │
│  │  │Ray │ │Cath│       │    │  │  Code Generator │ │                  │
│  │  │    │ │ie  │       │    │  └─────────────────┘ │                  │
│  │  └────┘ └────┘       │    └──────────────────────┘                  │
│  └──────────┬───────────┘                                              │
│             │                                                          │
│  ┌──────────▼───────────────────────────────────────────────────────┐  │
│  │                     MCP Tool Layer                                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │
│  │  │  Accounts   │  │   Market    │  │    Push     │               │  │
│  │  │   Server    │  │   Server    │  │   Server    │               │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     Data & Storage Layer                          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │
│  │  │   SQLite    │  │  ChromaDB   │  │  Polygon.io │               │  │
│  │  │  Database   │  │   Vector    │  │  Market API │               │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     Presentation Layer                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │
│  │  │   React     │  │   Gradio    │  │  REST API   │               │  │
│  │  │  Frontend   │  │  Dashboard  │  │  (FastAPI)  │               │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
Agentic AI/
│
├── agents/
│   │
│   ├── frameworks/                          # Learning & exploration implementations
│   │   ├── openai_sdk/                      # OpenAI Agents SDK tutorials
│   │   │   ├── agents_foundations_direct_llm_calls.ipynb
│   │   │   └── openai_agents_sdk.ipynb
│   │   ├── crewai/                          # CrewAI framework exploration
│   │   │   └── crewai_foundations.ipynb
│   │   ├── mcp/                             # Model Context Protocol examples
│   │   │   ├── foundations.ipynb
│   │   │   ├── accounts_server.py
│   │   │   ├── market_server.py
│   │   │   └── ...
│   │   ├── langchain/                       # LangChain explorations
│   │   ├── autogen/                         # Microsoft AutoGen examples
│   │   └── semantic_kernel/                 # Microsoft Semantic Kernel
│   │
│   └── projects/                            # Production-ready implementations
│       │
│       ├── autonomous_trading_system/       # Full-stack trading app (FastAPI + React)
│       │   ├── backend/                     # FastAPI backend service
│       │   │   └── app/
│       │   │       ├── api/                 # REST API endpoints
│       │   │       ├── core/                # Core configuration
│       │   │       ├── db/                  # Database models
│       │   │       ├── schemas/             # Pydantic schemas
│       │   │       └── services/            # Business logic
│       │   ├── frontend/                    # React TypeScript frontend
│       │   ├── data/                        # SQLite database
│       │   └── docs/                        # Documentation
│       │
│       ├── trading_agents_gradio/           # Gradio-based trading dashboard
│       │   ├── trading_floor.py             # Main orchestration
│       │   ├── traders.py                   # AI trader definitions
│       │   ├── accounts.py                  # Account management
│       │   ├── market.py                    # Market data integration
│       │   └── app.py                       # Gradio UI
│       │
│       ├── stock_picker/                    # CrewAI stock selection crew
│       ├── debate/                          # CrewAI AI debate system
│       ├── financial_researcher/            # CrewAI financial analysis
│       ├── engineering_team_crewai/         # CrewAI engineering automation
│       ├── engineering_team_fastapi/        # FastAPI engineering backend
│       ├── coder/                           # CrewAI code generation
│       └── my_assistant/                    # RAG chatbot with ChromaDB
│
├── pyproject.toml                           # Project configuration
├── requirements.txt                         # Python dependencies
├── .env                                     # Environment variables
└── README.md                                # This file
```

---

## Installation

### Prerequisites

- Python 3.12 or higher
- Node.js 18+ (for React frontend)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agentic-ai.git
   cd agentic-ai
   ```

2. **Set up Python environment**
   ```bash
   # Using uv (recommended)
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt

   # Or using pip
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Set up the frontend** (optional, for full-stack app)
   ```bash
   cd agents/projects/autonomous_trading_system/frontend
   npm install
   ```

---

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# LLM API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key

# Market Data
POLYGON_API_KEY=your_polygon_api_key

# Notifications
PUSHOVER_USER_KEY=your_pushover_user_key
PUSHOVER_API_TOKEN=your_pushover_api_token

# Search
SERPER_API_KEY=your_serper_api_key

# System Configuration
RUN_FREQUENCY_MINUTES=60
CHECK_MARKET_HOURS=true
```

---

## Usage

### Running the Autonomous Trading System

**Full-Stack Application (React + FastAPI)**
```bash
# Terminal 1: Start backend
cd agents/projects/autonomous_trading_system/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd agents/projects/autonomous_trading_system/frontend
npm run dev
```
Access at `http://localhost:5173`

**Gradio Dashboard**
```bash
cd agents/projects/trading_agents_gradio
python trading_floor.py
```
Access the dashboard at `http://localhost:7860`

### Running CrewAI Projects

**Stock Picker Crew**
```bash
cd agents/projects/stock_picker
python src/stock_picker/main.py
```

**Financial Researcher**
```bash
cd agents/projects/financial_researcher
python src/financial_researcher/main.py
```

**AI Debate System**
```bash
cd agents/projects/debate
python src/debate/main.py
```

### Running the AI Assistant

```bash
cd agents/projects/my_assistant
python chatbot.py
```

---

## Projects

| Project | Description | Tech Stack |
|---------|-------------|------------|
| **autonomous_trading_system** | Full-stack trading platform with 4 AI traders | FastAPI, React, SQLAlchemy, Polygon.io |
| **trading_agents_gradio** | Original Gradio-based trading dashboard | OpenAI Agents SDK, MCP, Gradio |
| **stock_picker** | Multi-agent stock selection system | CrewAI, Memory Integration |
| **debate** | AI debate and discussion platform | CrewAI, Multi-agent |
| **financial_researcher** | Deep financial analysis crew | CrewAI, Research Tools |
| **engineering_team_crewai** | Engineering task automation | CrewAI, Code Generation |
| **engineering_team_fastapi** | FastAPI backend for task management | FastAPI, SQLAlchemy |
| **coder** | AI code generation assistant | CrewAI, Developer Tools |
| **my_assistant** | RAG-enabled chatbot | OpenAI, ChromaDB, Gradio |

### Trading Agents

| Agent | Strategy | Risk Profile | Focus |
|-------|----------|--------------|-------|
| **Warren** | Value Investing | Conservative | Undervalued stocks, long-term holdings |
| **George** | Macro Trading | Aggressive | Market trends, contrarian bets |
| **Ray** | Risk Parity | Moderate | Diversification, systematic approach |
| **Cathie** | Innovation | High Risk | Tech stocks, cryptocurrency |

---

## Frameworks

The `agents/frameworks/` directory contains learning resources and exploration notebooks for various AI agent frameworks:

| Framework | Contents | Description |
|-----------|----------|-------------|
| **openai_sdk** | Jupyter notebooks | OpenAI Agents SDK foundations and examples |
| **crewai** | Jupyter notebooks | CrewAI multi-agent orchestration tutorials |
| **mcp** | Python files, notebooks | Model Context Protocol server/client examples |
| **langchain** | (empty) | Reserved for LangChain explorations |
| **autogen** | (empty) | Reserved for Microsoft AutoGen examples |
| **semantic_kernel** | (empty) | Reserved for Microsoft Semantic Kernel |

---

## Technologies

### AI/LLM Frameworks
- **OpenAI GPT-4/4o** - Primary language models
- **Anthropic Claude** - Advanced reasoning capabilities
- **CrewAI** - Multi-agent orchestration
- **LangChain/LangGraph** - Agent workflows and RAG
- **AutoGen** - Microsoft's agent framework
- **Semantic Kernel** - Microsoft's AI orchestration

### Backend
- **FastAPI** - High-performance REST API framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Material-UI** - Component library
- **Plotly** - Interactive charting
- **Gradio** - Rapid ML interface building

### Data & Integration
- **Polygon.io** - Real-time market data
- **ChromaDB** - Vector database for RAG
- **Model Context Protocol (MCP)** - Tool integration standard

---

## API Documentation

When running the backend, API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

```
GET  /api/v1/portfolio           # Get current portfolio
GET  /api/v1/traders             # List all traders
GET  /api/v1/traders/{id}        # Get trader details
POST /api/v1/trades              # Execute a trade
GET  /api/v1/market/prices       # Get current prices
GET  /api/v1/transactions        # Transaction history
```

---

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
# Format code
black .
isort .

# Type checking
mypy .
```

### Adding New Projects

1. Create a new folder in `agents/projects/`
2. Follow the existing project structure
3. Add project-specific README if needed
4. Update this main README with project details

### Adding Framework Explorations

1. Create notebooks/files in `agents/frameworks/<framework>/`
2. Document learnings and examples
3. Keep explorations separate from production projects

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed
- Keep commits atomic and well-described

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- OpenAI for GPT models and API
- Anthropic for Claude
- CrewAI team for the multi-agent framework
- Polygon.io for market data services
- The LangChain community

---

## Disclaimer

This software is for educational and research purposes only. The autonomous trading system is a demonstration of AI capabilities and should not be used for actual financial trading without proper risk assessment and regulatory compliance. The authors are not responsible for any financial losses incurred through the use of this software.

---

## Author

**Abhinav Sarkar**
- GitHub: [@AbhinavSarkarr](https://github.com/AbhinavSarkarr)
- LinkedIn: [abhinavsarkarrr](https://www.linkedin.com/in/abhinavsarkarrr)
- Portfolio: [abhinav-ai-portfolio.lovable.app](https://abhinav-ai-portfolio.lovable.app/)

---

<p align="center">
  <strong>Built with AI, for AI enthusiasts</strong>
</p>
