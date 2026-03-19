import pytest
import os
from unittest.mock import patch, MagicMock
from api.services.stream_service import StreamService

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {"STREAM_API_KEY": "mock_key", "STREAM_API_SECRET": "mock_secret"}):
        yield

@pytest.fixture
def stream_service(mock_env_vars):
    return StreamService()

def test_stream_service_initialization(stream_service):
    with patch("api.services.stream_service.StreamChat") as mock_chat, \
         patch("api.services.stream_service.Stream") as mock_feed:

        result = stream_service.initialize()

        assert result is True
        assert stream_service.chat_client is not None
        assert stream_service.feed_client is not None
        mock_chat.assert_called_once_with(api_key="mock_key", api_secret="mock_secret")
        mock_feed.assert_called_once_with(api_key="mock_key", api_secret="mock_secret")

def test_stream_service_initialization_no_credentials():
    with patch.dict(os.environ, clear=True):
        service = StreamService()
        result = service.initialize()

        assert result is False
        assert service.chat_client is None
        assert service.feed_client is None

def test_generate_chat_token(stream_service):
    stream_service.chat_client = MagicMock()
    stream_service.chat_client.create_token.return_value = "mock_chat_token"

    token = stream_service.generate_chat_token("user123")

    assert token == "mock_chat_token"
    stream_service.chat_client.create_token.assert_called_once_with("user123")

def test_generate_chat_token_uninitialized(stream_service):
    stream_service.chat_client = None
    token = stream_service.generate_chat_token("user123")
    assert token is None

def test_generate_feed_token(stream_service):
    stream_service.feed_client = MagicMock()
    stream_service.feed_client.create_user_token.return_value = "mock_feed_token"

    token = stream_service.generate_feed_token("user123")

    assert token == "mock_feed_token"
    stream_service.feed_client.create_user_token.assert_called_once_with("user123")

def test_generate_feed_token_uninitialized(stream_service):
    stream_service.feed_client = None
    token = stream_service.generate_feed_token("user123")
    assert token is None

def test_upsert_user(stream_service):
    stream_service.chat_client = MagicMock()
    stream_service.chat_client.upsert_user.return_value = None

    result = stream_service.upsert_user("user123", {"name": "Test User", "role": "trader"})

    assert result is True
    stream_service.chat_client.upsert_user.assert_called_once_with({
        "id": "user123",
        "name": "Test User",
        "role": "trader"
    })
