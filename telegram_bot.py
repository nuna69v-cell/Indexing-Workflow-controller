import os
import requests
import logging

logger = logging.getLogger("Integration.Telegram")

class TelegramAlerts:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_alert(self, message):
        if not self.token or not self.chat_id:
            logger.warning("Telegram credentials missing. Skipping alert.")
            return
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": f"🚨 GenX Alert: {message}"}
        
        try:
            requests.post(url, json=payload)
        except Exception as e:
            logger.error(f"Failed to send telegram alert: {e}")
