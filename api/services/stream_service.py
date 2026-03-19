import logging
import os
from typing import Any, Dict, Optional

from getstream import Stream
from stream_chat import StreamChat

logger = logging.getLogger(__name__)


class StreamService:
    def __init__(self):
        self.api_key = os.getenv("STREAM_API_KEY")
        self.api_secret = os.getenv("STREAM_API_SECRET")
        self.chat_client: Optional[StreamChat] = None
        self.feed_client: Optional[Stream] = None

    def initialize(self):
        if not self.api_key or not self.api_secret:
            logger.warning(
                "Stream API credentials not found. Stream services disabled."
            )
            return False

        try:
            # Initialize Chat Client
            self.chat_client = StreamChat(
                api_key=self.api_key, api_secret=self.api_secret
            )

            # Initialize Feeds Client
            self.feed_client = Stream(api_key=self.api_key, api_secret=self.api_secret)

            logger.info("Stream Chat and Feeds services initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Stream services: {e}")
            return False

    def generate_chat_token(self, user_id: str) -> Optional[str]:
        """Generate a secure token for a user to connect to Stream Chat"""
        if not self.chat_client:
            logger.error("Stream Chat client not initialized")
            return None

        try:
            return self.chat_client.create_token(user_id)
        except Exception as e:
            logger.error(f"Error generating chat token for {user_id}: {e}")
            return None

    def generate_feed_token(self, user_id: str) -> Optional[str]:
        """Generate a secure token for a user to connect to Stream Feeds"""
        if not self.feed_client:
            logger.error("Stream Feeds client not initialized")
            return None

        try:
            return self.feed_client.create_user_token(user_id)
        except Exception as e:
            logger.error(f"Error generating feed token for {user_id}: {e}")
            return None

    def upsert_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update or insert a user in Stream Chat"""
        if not self.chat_client:
            return False

        try:
            self.chat_client.upsert_user({"id": user_id, **data})
            return True
        except Exception as e:
            logger.error(f"Error upserting user {user_id}: {e}")
            return False


stream_service = StreamService()
