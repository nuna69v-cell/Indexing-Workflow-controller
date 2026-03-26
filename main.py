import os
import time
import logging
from brain.orchestrator import NodeOrchestrator
from brain.strategy_ai import StrategyAI
from brain.risk_ai import RiskAI
from integrations.market_data import MarketDataFeed
from shared.network_utils import get_local_ip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GenX-VisionOps")

def main():
    logger.info("Initializing GenX VisionOps Autonomous AI Trading Network...")
    logger.info(f"System IP: {get_local_ip()}")
    
    # Initialize Core Modules
    orchestrator = NodeOrchestrator()
    strategy_engine = StrategyAI()
    risk_manager = RiskAI()
    market_feed = MarketDataFeed()
    
    logger.info("Starting Distributed Nodes...")
    orchestrator.start_nodes()
    
    try:
        while True:
            # Main Loop
            health_status = orchestrator.check_health()
            logger.info(f"Network Health: {health_status}")
            
            # Market Update
            price_data = market_feed.get_latest_price("EURUSD")
            logger.info(f"Market Update: {price_data['symbol']} @ {price_data['price']}")
            
            # Risk Assessment
            if risk_manager.evaluate_global_risk():
                logger.warning("High Risk Detected! Adjusting strategies...")
                strategy_engine.optimize_allocation()
            
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down GenX VisionOps...")
        orchestrator.stop_all()

if __name__ == "__main__":
    main()
