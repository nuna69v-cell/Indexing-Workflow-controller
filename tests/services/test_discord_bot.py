import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Create a mock for aiohttp so the test can run even if it's missing or fails to import natively
mock_aiohttp = MagicMock()
mock_aiohttp.ClientError = Exception
sys.modules["aiohttp"] = mock_aiohttp

from services.discord_bot import DiscordBot  # noqa: E402


class MockResponse:
    def __init__(self, status):
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class MockSession:
    def __init__(self, post_return=None, post_exception=None):
        self.post_return = post_return
        self.post_exception = post_exception
        self.post_called_with = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def post(self, url, **kwargs):
        self.post_called_with = (url, kwargs)
        if self.post_exception:
            raise self.post_exception
        return self.post_return


class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        with patch.dict(os.environ, {"DISCORD_TOKEN": "test_token"}):
            self.discord_bot = DiscordBot()

    @patch("services.discord_bot.aiohttp.ClientSession")
    async def test_send_webhook_success(self, mock_client_session):
        test_url = "https://discord.com/api/webhooks/123/abc"
        test_content = "Test message"

        mock_response = MockResponse(204)
        mock_session = MockSession(post_return=mock_response)
        mock_client_session.return_value = mock_session

        result = await self.discord_bot.send_webhook(test_url, test_content)

        self.assertTrue(result)
        self.assertEqual(mock_session.post_called_with[0], test_url)
        self.assertEqual(
            mock_session.post_called_with[1], {"json": {"content": test_content}}
        )

    @patch("services.discord_bot.aiohttp.ClientSession")
    async def test_send_webhook_failure(self, mock_client_session):
        test_url = "https://discord.com/api/webhooks/123/abc"
        test_content = "Test message"

        mock_response = MockResponse(400)
        mock_session = MockSession(post_return=mock_response)
        mock_client_session.return_value = mock_session

        result = await self.discord_bot.send_webhook(test_url, test_content)

        self.assertFalse(result)

    @patch("services.discord_bot.aiohttp.ClientSession")
    async def test_send_webhook_exception(self, mock_client_session):
        test_url = "https://discord.com/api/webhooks/123/abc"
        test_content = "Test message"

        mock_session = MockSession(post_exception=Exception("Network error"))
        mock_client_session.return_value = mock_session

        with self.assertRaises(Exception):
            await self.discord_bot.send_webhook(test_url, test_content)


if __name__ == "__main__":
    unittest.main()
