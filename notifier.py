"""
Unified Notifier Service for GenX Trading Platform
Manages notifications across multiple channels (Telegram, Discord, WhatsApp, Matrix)
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class NotificationService:
    """Unified notification service for multiple channels"""

    def __init__(self):
        """Initialize notification service with all available channels"""
        self.channels = []
        self._initialize_channels()

    def _initialize_channels(self):
        """Initialize all available notification channels"""
        # Import channel modules
        try:
            from services.telegram_bot import telegram_bot

            if telegram_bot.enabled:
                self.channels.append(("telegram", telegram_bot))
                logger.info("Telegram channel initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Telegram: {e}")

        try:
            from services.discord_bot import discord_bot

            if discord_bot.enabled:
                self.channels.append(("discord", discord_bot))
                logger.info("Discord channel initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Discord: {e}")

        try:
            from services.whatsapp_bot import whatsapp_bot

            if whatsapp_bot.enabled:
                self.channels.append(("whatsapp", whatsapp_bot))
                logger.info("WhatsApp channel initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize WhatsApp: {e}")

        try:
            from services.matrix_bot import matrix_bot

            if matrix_bot.enabled:
                self.channels.append(("matrix", matrix_bot))
                logger.info("Matrix channel initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Matrix: {e}")

        if not self.channels:
            logger.warning("No notification channels are configured!")

    def send_signal(self, signal: Dict) -> Dict[str, bool]:
        """Send trading signal to all configured channels"""
        results = {}
        for channel_name, channel_bot in self.channels:
            try:
                success = channel_bot.send_signal(signal)
                results[channel_name] = success
            except Exception as e:
                logger.error(f"Error sending signal to {channel_name}: {e}")
                results[channel_name] = False
        return results

    def send_image(self, file_path: str, caption: str = "") -> Dict[str, bool]:
        """Send an image to all supported channels"""
        results = {}
        for channel_name, channel_bot in self.channels:
            try:
                if hasattr(channel_bot, "send_image"):
                    success = channel_bot.send_image(file_path, caption)
                    results[channel_name] = success
                else:
                    logger.debug(f"Channel {channel_name} does not support images")
            except Exception as e:
                logger.error(f"Error sending image to {channel_name}: {e}")
                results[channel_name] = False
        return results

    def send_notification(
        self, title: str, message: str, channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send a notification to specified or all channels"""
        results = {}
        for channel_name, channel_bot in self.channels:
            if channels and channel_name not in channels:
                continue
            try:
                success = channel_bot.send_notification(title, message)
                results[channel_name] = success
            except Exception as e:
                logger.error(f"Error sending notification to {channel_name}: {e}")
                results[channel_name] = False
        return results

    def send_status_update(
        self, service_name: str, status: str, details: str = ""
    ) -> Dict[str, bool]:
        """Send a status update to all configured channels"""
        results = {}
        for channel_name, channel_bot in self.channels:
            try:
                success = channel_bot.send_status_update(service_name, status, details)
                results[channel_name] = success
            except Exception as e:
                logger.error(f"Error sending status update to {channel_name}: {e}")
                results[channel_name] = False
        return results

    def get_active_channels(self) -> List[str]:
        """Get list of active channel names"""
        return [name for name, _ in self.channels]


# Create singleton instance
notifier = NotificationService()


def send_signal(signal: Dict) -> Dict[str, bool]:
    return notifier.send_signal(signal)


def send_image(file_path: str, caption: str = "") -> Dict[str, bool]:
    return notifier.send_image(file_path, caption)


def send_notification(
    title: str, message: str, channels: Optional[List[str]] = None
) -> Dict[str, bool]:
    return notifier.send_notification(title, message, channels)


def send_status_update(
    service_name: str, status: str, details: str = ""
) -> Dict[str, bool]:
    return notifier.send_status_update(service_name, status, details)
