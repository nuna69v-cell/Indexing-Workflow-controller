import os
import sys
from unittest.mock import MagicMock

import pytest

# Set testing environment variables before any application code is imported
os.environ["TESTING"] = "true"
os.environ["EA_API_KEY"] = "test_api_key_12345"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["JWT_SECRET"] = "test_jwt_secret"

try:
    import talib
except ImportError:
    import numpy as np
    import pandas as pd

    class MockTalib:
        def SMA(self, arr, timeperiod=None):
            if isinstance(arr, pd.Series):
                arr = arr.values
            return np.zeros_like(arr)

        def RSI(self, arr, timeperiod=None):
            return pd.Series(
                np.zeros_like(arr)
                if isinstance(arr, np.ndarray)
                else np.zeros(len(arr))
            )

        def MACD(self, arr):
            res = pd.Series(
                np.zeros_like(arr)
                if isinstance(arr, np.ndarray)
                else np.zeros(len(arr))
            )
            return res, res, res

        def ATR(self, h, l, c, timeperiod=None):
            return pd.Series(
                np.zeros_like(c) if isinstance(c, np.ndarray) else np.zeros(len(c))
            )

        def ADX(self, h, l, c, timeperiod=None):
            return pd.Series(
                np.zeros_like(c) if isinstance(c, np.ndarray) else np.zeros(len(c))
            )

        def BBANDS(self, arr):
            res = pd.Series(
                np.zeros_like(arr)
                if isinstance(arr, np.ndarray)
                else np.zeros(len(arr))
            )
            return res, res, res

        def STOCH(self, h, l, c):
            res = pd.Series(
                np.zeros_like(c) if isinstance(c, np.ndarray) else np.zeros(len(c))
            )
            return res, res

        def CDL2CROWS(self, o, h, l, c):
            return pd.Series(
                np.zeros_like(c) if isinstance(c, np.ndarray) else np.zeros(len(c))
            )

        def __getattr__(self, name):
            if name.startswith("CDL"):
                return lambda o, h, l, c: pd.Series(
                    np.zeros_like(c) if isinstance(c, np.ndarray) else np.zeros(len(c))
                )
            return lambda *args, **kwargs: pd.Series(
                np.zeros_like(args[0])
                if isinstance(args[0], np.ndarray)
                else np.zeros(len(args[0]))
            )

    sys.modules["talib"] = MockTalib()


@pytest.fixture(autouse=True)
def clear_ea_state():
    """Clear global state in ea_http router between tests."""
    try:
        from api.routers import ea_http

        ea_http.ea_connections = {}
        from collections import deque

        ea_http.pending_signals = deque()
        ea_http.trade_results = []
    except ImportError:
        pass
