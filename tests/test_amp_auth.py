import sys
import os
from unittest.mock import patch

# Add the root directory to sys.path so we can import amp_auth
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from amp_auth import authenticate_user


@patch("amp_auth.amp_auth.authenticate")
def test_authenticate_user(mock_authenticate):
    # Setup
    token = "test_token"
    mock_authenticate.return_value = True

    # Execution
    result = authenticate_user(token)

    # Verification
    mock_authenticate.assert_called_once_with(token)
    assert result is True


@patch("amp_auth.amp_auth.authenticate")
def test_authenticate_user_failure(mock_authenticate):
    # Setup
    token = "invalid_token"
    mock_authenticate.return_value = False

    # Execution
    result = authenticate_user(token)

    # Verification
    mock_authenticate.assert_called_once_with(token)
    assert result is False
