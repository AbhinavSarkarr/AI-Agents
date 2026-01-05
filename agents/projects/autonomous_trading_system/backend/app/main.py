"""
FastAPI application for the Autonomous Trading Agentic System.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from .core.config import settings
from .core.database import DatabaseManager
from .api.routes import accounts, trading, market, system, agents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    print("🚀 Starting Autonomous Trading Agentic System...")
    
    # Initialize database
    DatabaseManager.init_database()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Autonomous Trading Agentic System",
    description="A sophisticated multi-agent trading system with AI-powered portfolio management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(trading.router, prefix="/api/trading", tags=["trading"])
app.include_router(market.router, prefix="/api/market", tags=["market"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])

# Mount static files (for serving the React build)
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Autonomous Trading Agentic System API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2025-01-01T00:00:00Z"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )