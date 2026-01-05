# Autonomous Trading Agentic System

A sophisticated multi-agent autonomous stock trading system featuring 4 AI traders with distinct personalities and strategies. Built with FastAPI backend and React frontend for real-time portfolio management and monitoring.

## 🏗️ Architecture

```
Autonomous Trading Agentic System/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # REST API endpoints
│   │   ├── core/              # Core business logic
│   │   ├── models/            # Database models
│   │   ├── services/          # Business services
│   │   └── utils/             # Utility functions
│   ├── tests/                 # Backend tests
│   └── scripts/               # Management scripts
├── frontend/                   # React TypeScript frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Main pages
│   │   ├── services/          # API clients
│   │   ├── hooks/             # Custom React hooks
│   │   ├── utils/             # Frontend utilities
│   │   └── types/             # TypeScript definitions
│   ├── public/                # Static assets
│   └── tests/                 # Frontend tests
├── docs/                      # Documentation
├── data/                      # Database and data files
└── logs/                      # Application logs
```

## 🤖 The Four Trading Agents

- **Warren** (Patience) - Value investing inspired by Warren Buffett
- **George** (Bold) - Macro trading inspired by George Soros
- **Ray** (Systematic) - Risk parity inspired by Ray Dalio
- **Cathie** (Crypto) - Innovation focus inspired by Cathie Wood

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Polygon.io API key

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your API keys
python scripts/init_db.py
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📊 Features

- **Real-time Portfolio Monitoring** - Live updates via WebSocket
- **AI Agent Management** - Monitor and control trading agents
- **Market Data Integration** - Polygon.io API for real market data
- **Performance Analytics** - Detailed P&L tracking and visualization
- **Risk Management** - Built-in position sizing and constraints
- **Push Notifications** - Mobile alerts for trading activity
- **Persistent Memory** - Agents learn from past decisions
- **Multi-Model Support** - GPT, DeepSeek, Gemini, Grok integration

## 🔧 Configuration

Set environment variables in `backend/.env`:
```
POLYGON_API_KEY=your_polygon_api_key
POLYGON_PLAN=free  # or paid/realtime
SERPER_API_KEY=your_serper_api_key
PUSHOVER_USER=your_pushover_user
PUSHOVER_TOKEN=your_pushover_token
RUN_EVERY_N_MINUTES=60
RUN_EVEN_WHEN_MARKET_IS_CLOSED=false
USE_MANY_MODELS=false
```

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Agent Strategies](docs/AGENTS.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🧪 Testing

```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm test
```

## 📈 Performance

The system can handle:
- 4 concurrent AI agents
- Real-time market data processing
- WebSocket connections for live updates
- Persistent storage of all transactions and decisions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.