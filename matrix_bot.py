import aiohttp
import asyncio
import logging
import os
import mimetypes
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class MatrixBot:
    """Matrix (Element) notification channel"""

    def __init__(self):
        self.homeserver = os.getenv("MATRIX_HOMESERVER", "https://matrix.org")
        self.access_token = os.getenv("MATRIX_ACCESS_TOKEN", None)
        self.room_id = os.getenv("MATRIX_ROOM_ID", None)
        self.enabled = all([self.access_token, self.room_id])

        if self.enabled:
            logger.info("Matrix bot initialized and enabled")
        else:
            logger.info("Matrix bot is disabled (missing credentials)")

    async def _upload_content(self, file_path: str) -> Optional[str]:
        """Upload file to Matrix media repository and return MXC URI"""
        if not self.enabled or not os.path.exists(file_path):
            return None

        url = f"{self.homeserver}/_matrix/media/v3/upload"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": mimetypes.guess_type(file_path)[0]
            or "application/octet-stream",
        }

        filename = os.path.basename(file_path)
        params = {"filename": filename}

        try:
            async with aiohttp.ClientSession() as session:
                with open(file_path, "rb") as f:
                    async with session.post(
                        url, data=f, headers=headers, params=params
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data.get("content_uri")
                        else:
                            error_text = await response.text()
                            logger.error(
                                f"Matrix upload error: {response.status} - {error_text}"
                            )
                            return None
        except Exception as e:
            logger.error(f"Matrix upload failed: {e}")
            return None

    async def _send_request(
        self, message: str, content_type: str = "m.text", extra: dict = None
    ) -> bool:
        """Send message via Matrix Client-Server API"""
        if not self.enabled:
            return False

        url = f"{self.homeserver}/_matrix/client/v3/rooms/{self.room_id}/send/m.room.message"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        payload = {"msgtype": content_type, "body": message}
        if extra:
            payload.update(extra)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"Matrix API error: {response.status} - {error_text}"
                        )
                        return False
        except Exception as e:
            logger.error(f"Matrix request failed: {e}")
            return False

    def send_image(self, file_path: str, caption: str = "") -> bool:
        """Upload and send an image to Matrix"""
        if not self.enabled:
            return False

        async def run_upload_and_send():
            mxc_uri = await self._upload_content(file_path)
            if not mxc_uri:
                return False

            extra = {
                "url": mxc_uri,
                "info": {"mimetype": mimetypes.guess_type(file_path)[0] or "image/png"},
            }
            return await self._send_request(
                caption or os.path.basename(file_path), "m.image", extra
            )

        try:
            return asyncio.run(run_upload_and_send())
        except Exception:
            return False

    def send_signal(self, signal: Dict) -> bool:
        """Send trading signal to Matrix"""
        message = (
            f"🚀 **New Signal: {signal.get('symbol')}**\n"
            f"Type: {signal.get('type')}\n"
            f"Entry: {signal.get('entry')}\n"
            f"SL: {signal.get('sl')}\n"
            f"TP: {signal.get('tp')}\n"
            f"Risk: {signal.get('risk_percent')}%"
        )
        try:
            return asyncio.run(self._send_request(message))
        except Exception:
            return False

    def send_notification(self, title: str, message: str) -> bool:
        """Send general notification to Matrix"""
        full_message = f"🔔 **{title}**\n{message}"
        try:
            return asyncio.run(self._send_request(full_message))
        except Exception:
            return False

    def send_status_update(
        self, service_name: str, status: str, details: str = ""
    ) -> bool:
        """Send status update to Matrix"""
        message = f"📊 **Status Update: {service_name}**\nStatus: {status}\n{details}"
        try:
            return asyncio.run(self._send_request(message))
        except Exception:
            return False


# Create singleton instance
matrix_bot = MatrixBot()
