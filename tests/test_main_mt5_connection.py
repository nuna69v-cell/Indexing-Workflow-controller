import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.modules['dotenv'] = MagicMock()

# Import the module under test
import main


def test_check_mt5_connection_path_not_exists(caplog):
    """Test when the MT5 terminal path does not exist."""
    with patch("os.path.exists", return_value=False):
        with patch("os.getenv", return_value="/invalid/path"):
            result = main.check_mt5_connection()
            assert result is False
            assert "MT5 terminal path not found" in caplog.text


def test_check_mt5_connection_import_error(caplog):
    """Test when path exists but MetaTrader5 package is not available (e.g., Linux)."""
    with patch("os.path.exists", return_value=True):
        # We simulate ImportError when attempting to import MetaTrader5 inside the function
        # Since it's imported locally, we can patch sys.modules to raise ImportError
        # Or simpler, patch builtins.__import__

        # We need a custom import mock
        original_import = __import__

        def mock_import(name, *args, **kwargs):
            if name == 'MetaTrader5':
                raise ImportError("No module named 'MetaTrader5'")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            result = main.check_mt5_connection()
            assert result is True
            assert "MetaTrader5 package not installed or not supported on this OS" in caplog.text


@patch.dict('sys.modules', {'MetaTrader5': MagicMock()})
def test_check_mt5_connection_initialization_fails(caplog):
    """Test when MetaTrader5 is available but initialization fails."""
    # Since we patched sys.modules, 'import MetaTrader5' will return the MagicMock
    import MetaTrader5 as mt5

    # Configure the mock
    mt5.initialize.return_value = False
    mt5.last_error.return_value = (-1000, "Some error")

    with patch("os.path.exists", return_value=True):
        result = main.check_mt5_connection()
        assert result is False
        assert "MT5 initialization failed" in caplog.text


@patch.dict('sys.modules', {'MetaTrader5': MagicMock()})
def test_check_mt5_connection_not_connected(caplog):
    """Test when MT5 initializes but terminal is not connected to broker."""
    import MetaTrader5 as mt5

    # Configure the mock
    mt5.initialize.return_value = True

    # terminal_info returns an object with a 'connected' attribute
    mock_terminal_info = MagicMock()
    mock_terminal_info.connected = False
    mt5.terminal_info.return_value = mock_terminal_info

    with patch("os.path.exists", return_value=True):
        result = main.check_mt5_connection()
        assert result is False
        assert "MT5 terminal is not connected to broker" in caplog.text
        mt5.shutdown.assert_called_once()


@patch.dict('sys.modules', {'MetaTrader5': MagicMock()})
def test_check_mt5_connection_success(caplog):
    """Test when MT5 initializes successfully and terminal is connected."""
    caplog.set_level('INFO')
    import MetaTrader5 as mt5

    # Configure the mock
    mt5.initialize.return_value = True

    mock_terminal_info = MagicMock()
    mock_terminal_info.connected = True
    mt5.terminal_info.return_value = mock_terminal_info

    with patch("os.path.exists", return_value=True):
        result = main.check_mt5_connection()
        assert result is True
        assert "Successfully connected to MT5 terminal" in caplog.text
        mt5.shutdown.assert_called_once()


@patch.dict('sys.modules', {'MetaTrader5': MagicMock()})
def test_check_mt5_connection_exception(caplog):
    """Test when an unexpected exception occurs during connection check."""
    import MetaTrader5 as mt5

    # Make initialize raise an Exception
    mt5.initialize.side_effect = Exception("Unexpected failure")

    with patch("os.path.exists", return_value=True):
        result = main.check_mt5_connection()
        assert result is False
        assert "Error checking MT5 connection: Unexpected failure" in caplog.text
