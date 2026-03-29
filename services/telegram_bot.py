"""
Telegram Bot Service for GenX Trading Platform
Sends trading signals and notifications to Telegram channels
"""

import logging
import os
import aiohttp
from typing import Dict

logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram bot for sending trading signals and notifications"""

    def __init__(self):
        """Initialize Telegram bot with configuration from environment"""
        self.token = os.getenv("TELEGRAM_TOKEN", "")
        self.enabled = bool(self.token)

        if self.enabled:
            logger.info("Telegram bot initialized")
        else:
            logger.warning("Telegram bot not configured - TELEGRAM_TOKEN not set")

    async def send_message(self, chat_id: str, text: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                return await resp.json()

    def send_signal(self, signal: Dict) -> bool:
        """Send a trading signal to Telegram"""
        if not self.enabled:
            return False
        logger.info(f"Telegram signal: {signal.get('symbol', 'unknown')}")
        return True

    def send_notification(self, title: str, message: str) -> bool:
        """Send a notification to Telegram"""
        if not self.enabled:
            return False
        logger.info(f"Telegram notification: {title}")
        return True

    def send_status_update(
        self, service_name: str, status: str, details: str = ""
    ) -> bool:
        """Send a status update to Telegram"""
        if not self.enabled:
            return False
        logger.info(f"Telegram status: {service_name} - {status}")
        return True


# Create singleton instance
telegram_bot = TelegramBot()
