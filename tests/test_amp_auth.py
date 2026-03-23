from unittest.mock import MagicMock
import pytest
from amp_auth import AMPAuth

def test_authenticate_success():
    auth = AMPAuth()

    # Mock parse_token to return a valid dict
    auth.parse_token = MagicMock(return_value={'user_id': 'test_user_123', 'session_hash': 'abc'})

    # Mock _validate_token to return True
    auth._validate_token = MagicMock(return_value=True)

    # Execute
    result = auth.authenticate("some_token")

    # Verify
    assert result is True
    assert auth.is_logged_in is True
    assert auth.current_user == 'test_user_123'

    # Verify mocks were called
    auth.parse_token.assert_called_once_with("some_token")
    auth._validate_token.assert_called_once_with({'user_id': 'test_user_123', 'session_hash': 'abc'})

def test_authenticate_invalid_token():
    auth = AMPAuth()

    # Mock parse_token to return an empty dict/None (invalid token)
    auth.parse_token = MagicMock(return_value={})

    # Mock _validate_token
    auth._validate_token = MagicMock()

    # Execute
    result = auth.authenticate("invalid_token")

    # Verify
    assert result is False
    assert auth.is_logged_in is False
    assert auth.current_user is None

    # Verify mocks
    auth.parse_token.assert_called_once_with("invalid_token")
    auth._validate_token.assert_not_called()

def test_authenticate_validation_failed():
    auth = AMPAuth()

    # Mock parse_token to return a valid dict
    auth.parse_token = MagicMock(return_value={'user_id': 'test_user_123', 'session_hash': 'abc'})

    # Mock _validate_token to return False (validation failed)
    auth._validate_token = MagicMock(return_value=False)

    # Execute
    result = auth.authenticate("some_token")

    # Verify
    assert result is False
    assert auth.is_logged_in is False
    assert auth.current_user is None

    # Verify mocks
    auth.parse_token.assert_called_once_with("some_token")
    auth._validate_token.assert_called_once_with({'user_id': 'test_user_123', 'session_hash': 'abc'})
