"""Market data service for fetching and caching stock prices."""

import random
from datetime import datetime, date, timezone
from typing import Optional, Dict, List
from functools import lru_cache
from sqlalchemy.orm import Session

try:
    from polygon import RESTClient
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False

from ..models.market_data import MarketData
from ..core.config import settings


class MarketService:
    """Service for fetching and managing market data."""
    
    def __init__(self, db: Session):
        self.db = db
        self._polygon_client = None
        
    @property
    def polygon_client(self) -> Optional['RESTClient']:
        """Get Polygon client if available."""
        if not POLYGON_AVAILABLE or not settings.polygon_api_key:
            return None
            
        if not self._polygon_client:
            self._polygon_client = RESTClient(settings.polygon_api_key)
        return self._polygon_client
    
    def is_market_open(self) -> bool:
        """Check if the market is currently open."""
        if not self.polygon_client:
            # Default to market hours if no API
            now = datetime.now().time()
            return now.hour >= 9 and now.hour < 16  # 9 AM to 4 PM
        
        try:
            market_status = self.polygon_client.get_market_status()
            return market_status.market == "open"
        except Exception:
            return False
    
    def get_share_price(self, symbol: str) -> float:
        """Get current share price for a symbol."""
        if settings.polygon_api_key and self.polygon_client:
            try:
                return self._get_share_price_polygon(symbol)
            except Exception as e:
                print(f"Error fetching price from Polygon API: {e}")
        
        # Fallback to cached data or random price
        cached_price = self._get_cached_price(symbol)
        if cached_price is not None:
            return cached_price
            
        return float(random.randint(1, 100))  # Random fallback
    
    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Get prices for multiple symbols."""
        prices = {}
        for symbol in symbols:
            prices[symbol] = self.get_share_price(symbol)
        return prices
    
    def _get_share_price_polygon(self, symbol: str) -> float:
        """Get share price from Polygon API."""
        if settings.is_paid_polygon or settings.is_realtime_polygon:
            return self._get_share_price_polygon_realtime(symbol)
        else:
            return self._get_share_price_polygon_eod(symbol)
    
    def _get_share_price_polygon_realtime(self, symbol: str) -> float:
        """Get real-time or delayed price from Polygon."""
        if not self.polygon_client:
            raise ValueError("Polygon client not available")
            
        result = self.polygon_client.get_snapshot_ticker("stocks", symbol)
        return result.min.close or result.prev_day.close
    
    def _get_share_price_polygon_eod(self, symbol: str) -> float:
        """Get end-of-day price from Polygon."""
        today = datetime.now().date().strftime("%Y-%m-%d")
        market_data = self._get_market_data_for_date(today)
        return market_data.get(symbol, 0.0)
    
    @lru_cache(maxsize=2)
    def _get_market_data_for_date(self, date_str: str) -> Dict[str, float]:
        """Get cached market data for a specific date."""
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Check cache first
        cached_data = self._get_cached_market_data(target_date)
        if cached_data:
            return cached_data
        
        # Fetch from Polygon if available
        if self.polygon_client:
            try:
                fresh_data = self._fetch_all_share_prices_polygon_eod()
                self._cache_market_data(target_date, fresh_data)
                return fresh_data
            except Exception as e:
                print(f"Error fetching market data: {e}")
        
        return {}
    
    def _fetch_all_share_prices_polygon_eod(self) -> Dict[str, float]:
        """Fetch all share prices for end-of-day."""
        if not self.polygon_client:
            return {}
            
        # Get the last close date
        probe = self.polygon_client.get_previous_close_agg("SPY")[0]
        last_close = datetime.fromtimestamp(probe.timestamp / 1000, tz=timezone.utc).date()
        
        # Get grouped daily aggregates
        results = self.polygon_client.get_grouped_daily_aggs(last_close, adjusted=True, include_otc=False)
        return {result.ticker: result.close for result in results}
    
    def _get_cached_price(self, symbol: str) -> Optional[float]:
        """Get cached price for a symbol."""
        today = date.today()
        
        # Try today first, then previous days
        for days_back in range(5):
            check_date = date.fromordinal(today.toordinal() - days_back)
            market_data = (
                self.db.query(MarketData)
                .filter(
                    MarketData.symbol == symbol.upper(),
                    MarketData.date == check_date
                )
                .first()
            )
            
            if market_data and not market_data.is_stale(24):
                return market_data.close_price
        
        return None
    
    def _get_cached_market_data(self, target_date: date) -> Optional[Dict[str, float]]:
        """Get all cached market data for a date."""
        market_data_records = (
            self.db.query(MarketData)
            .filter(MarketData.date == target_date)
            .all()
        )
        
        if not market_data_records:
            return None
            
        # Check if data is fresh
        if any(record.is_stale(24) for record in market_data_records):
            return None
            
        return {record.symbol: record.close_price for record in market_data_records}
    
    def _cache_market_data(self, target_date: date, price_data: Dict[str, float]) -> None:
        """Cache market data in database."""
        for symbol, price in price_data.items():
            # Check if record already exists
            existing = (
                self.db.query(MarketData)
                .filter(
                    MarketData.symbol == symbol,
                    MarketData.date == target_date
                )
                .first()
            )
            
            if existing:
                # Update existing record
                existing.close_price = price
                existing.fetched_at = datetime.utcnow()
                existing.data_quality = "good"
            else:
                # Create new record
                market_data = MarketData.create_eod_record(
                    symbol=symbol,
                    date=target_date,
                    close_price=price
                )
                self.db.add(market_data)
        
        self.db.commit()
    
    def update_market_data(self, symbol: str, price_data: dict) -> MarketData:
        """Update market data for a symbol."""
        today = date.today()
        
        market_data = MarketData(
            symbol=symbol.upper(),
            date=today,
            close_price=price_data.get("close", 0.0),
            open_price=price_data.get("open"),
            high_price=price_data.get("high"),
            low_price=price_data.get("low"),
            volume=price_data.get("volume"),
            data_source="manual"
        )
        
        self.db.add(market_data)
        self.db.commit()
        self.db.refresh(market_data)
        return market_data
    
    def get_market_summary(self) -> Dict:
        """Get market summary statistics."""
        today = date.today()
        
        # Get today's market data count
        todays_data_count = (
            self.db.query(MarketData)
            .filter(MarketData.date == today)
            .count()
        )
        
        return {
            "date": today.isoformat(),
            "market_open": self.is_market_open(),
            "symbols_updated_today": todays_data_count,
            "polygon_api_available": POLYGON_AVAILABLE and bool(settings.polygon_api_key),
            "polygon_plan": settings.polygon_plan,
            "data_sources": ["polygon", "cache", "random_fallback"]
        }