import logging

logger = logging.getLogger("Brain.RiskAI")

class RiskAI:
    def __init__(self):
        self.max_drawdown = 0.05  # 5%
        self.current_drawdown = 0.01

    def evaluate_global_risk(self):
        # Simulate risk check
        if self.current_drawdown > self.max_drawdown:
            logger.error("CRITICAL: Max drawdown exceeded!")
            return True
        return False
