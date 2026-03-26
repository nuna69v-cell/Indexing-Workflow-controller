import random
import logging
from datetime import datetime

logger = logging.getLogger("Integration.MarketData")

class MarketDataFeed:
    def __init__(self):
        self.providers = ["Binance", "OANDA", "Coinbase"]
        self.active_provider = "Binance"
        logger.info(f"Market Data Feed initialized with {self.active_provider}")

    def get_latest_price(self, symbol):
        # Simulated price generation
        base_prices = {
            "BTCUSDT": 65000.0,
            "ETHUSDT": 3500.0,
            "EURUSD": 1.0850,
            "XAUUSD": 2150.0
        }
        
        base = base_prices.get(symbol, 100.0)
        volatility = 0.001
        price = base + (random.random() - 0.5) * base * volatility
        
        return {
            "symbol": symbol,
            "price": round(price, 5),
            "timestamp": datetime.now().isoformat(),
            "provider": self.active_provider
        }

    def subscribe_to_ticker(self, symbol, callback):
        logger.info(f"Subscribed to real-time ticker for {symbol}")
        # In a real app, this would start a websocket connection
        pass
