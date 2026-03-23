import pytest
from unittest.mock import patch, MagicMock, AsyncMock

# Import the module to be tested
from services.telegram_bot import TelegramBot


@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to mock environment variables."""
    monkeypatch.setenv("TELEGRAM_TOKEN", "test_token")


@pytest.fixture
def mock_aiohttp_session():
    """Fixture to mock aiohttp ClientSession and its context managers."""
    # Create the top-level mock for aiohttp.ClientSession
    with patch("aiohttp.ClientSession") as mock_session_cls:
        # Create a mock instance of the session
        mock_session_instance = MagicMock()

        # Make the class return our mock instance when called
        mock_session_cls.return_value = mock_session_instance

        # Set up the async context manager for the session:
        # async with aiohttp.ClientSession() as session:
        mock_session_instance.__aenter__.return_value = mock_session_instance

        # Create a mock for the response
        mock_response = MagicMock()
        mock_response.json = AsyncMock(
            return_value={"ok": True, "result": {"message_id": 123}}
        )

        # Set up the async context manager for the post request:
        # async with session.post(...) as resp:
        mock_post_context = MagicMock()
        mock_post_context.__aenter__.return_value = mock_response
        mock_session_instance.post.return_value = mock_post_context

        yield {
            "session_cls": mock_session_cls,
            "session_instance": mock_session_instance,
            "post_context": mock_post_context,
            "response": mock_response,
        }


@pytest.mark.asyncio
async def test_send_message_success(mock_env, mock_aiohttp_session):
    """Test successful message sending."""
    bot = TelegramBot()
    chat_id = "123456789"
    text = "Hello, World!"

    result = await bot.send_message(chat_id, text)

    # Assertions
    assert result == {"ok": True, "result": {"message_id": 123}}

    # Verify aiohttp was called correctly
    mock_session_instance = mock_aiohttp_session["session_instance"]
    mock_session_instance.post.assert_called_once_with(
        "https://api.telegram.org/bottest_token/sendMessage",
        json={"chat_id": chat_id, "text": text},
    )

    # Verify response.json() was called
    mock_response = mock_aiohttp_session["response"]
    mock_response.json.assert_called_once()


@pytest.mark.asyncio
async def test_send_message_error(mock_env, mock_aiohttp_session):
    """Test message sending when API returns an error."""
    # Override the mock response to return an error
    mock_response = mock_aiohttp_session["response"]
    mock_response.json = AsyncMock(
        return_value={"ok": False, "error_code": 400, "description": "Bad Request"}
    )

    bot = TelegramBot()
    chat_id = "invalid_chat"
    text = "Hello!"

    result = await bot.send_message(chat_id, text)

    assert result == {"ok": False, "error_code": 400, "description": "Bad Request"}


def test_init_with_token(mock_env):
    """Test initialization when TELEGRAM_TOKEN is set."""
    bot = TelegramBot()
    assert bot.token == "test_token"
    assert bot.enabled is True


def test_init_without_token(monkeypatch):
    """Test initialization when TELEGRAM_TOKEN is not set."""
    monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
    bot = TelegramBot()
    assert bot.token == ""
    assert bot.enabled is False


def test_send_signal_enabled(mock_env):
    """Test send_signal when bot is enabled."""
    bot = TelegramBot()
    result = bot.send_signal({"symbol": "EURUSD", "action": "BUY"})
    assert result is True


def test_send_signal_disabled(monkeypatch):
    """Test send_signal when bot is disabled."""
    monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
    bot = TelegramBot()
    result = bot.send_signal({"symbol": "EURUSD"})
    assert result is False


def test_send_notification_enabled(mock_env):
    """Test send_notification when bot is enabled."""
    bot = TelegramBot()
    result = bot.send_notification("Title", "Message")
    assert result is True


def test_send_status_update_enabled(mock_env):
    """Test send_status_update when bot is enabled."""
    bot = TelegramBot()
    result = bot.send_status_update("Service", "Status")
    assert result is True
