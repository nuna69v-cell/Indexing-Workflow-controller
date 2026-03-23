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
    import talib  # noqa: F401







except ImportError:
    import numpy as np
    import pandas as pd

    class MockMAType:
        SMA = 0
        EMA = 1
        WMA = 2
        DEMA = 3
        TEMA = 4
        TRIMA = 5
        KAMA = 6
        MAMA = 7
        T3 = 8

    class MockAbstract:
        TA_FUNC_FLAGS = {}
        TA_OUTPUT_FLAGS = {}


    class MockTalib:
        MA_Type = MockMAType()
        abstract = MockAbstract()
        def get_functions(self):
            return []
        def SMA(self, arr, timeperiod=None):
            if isinstance(arr, pd.Series): return pd.Series(np.ones_like(arr.values))
            return np.ones_like(arr)
        def EMA(self, arr, timeperiod=None):
            if isinstance(arr, pd.Series): return pd.Series(np.ones_like(arr.values))
            return np.ones_like(arr)
        def RSI(self, arr, timeperiod=None):
            if isinstance(arr, pd.Series): return pd.Series(np.ones_like(arr.values))
            return np.ones_like(arr)
        def MACD(self, arr, fastperiod=None, slowperiod=None, signalperiod=None):
            if isinstance(arr, pd.Series): return pd.Series(np.ones_like(arr.values)), pd.Series(np.ones_like(arr.values)), pd.Series(np.ones_like(arr.values))
            return np.ones_like(arr), np.ones_like(arr), np.ones_like(arr)
        def ATR(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def NATR(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def MFI(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def ADX(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def PLUS_DI(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def MINUS_DI(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def CCI(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def OBV(self, close, volume, timeperiod=None):
            return np.ones_like(close)
        def WILLR(self, high, low, close, timeperiod=None):
            return np.ones_like(close)
        def BBANDS(self, close, timeperiod=None, nbdevup=None, nbdevdn=None, matype=None):
            return np.ones_like(close), np.ones_like(close), np.ones_like(close)
        def MACDEXT(self, close, fastperiod=None, fastmatype=None, slowperiod=None, slowmatype=None, signalperiod=None, signalmatype=None):
            return np.ones_like(close), np.ones_like(close), np.ones_like(close)
        def STOCH(self, high, low, close, fastk_period=None, slowk_period=None, slowk_matype=None, slowd_period=None, slowd_matype=None):
            return np.ones_like(close), np.ones_like(close)
        def MOM(self, arr, timeperiod=None):
            if isinstance(arr, pd.Series): return pd.Series(np.ones_like(arr.values))
            return np.ones_like(arr)
        def ROC(self, arr, timeperiod=None):
            if isinstance(arr, pd.Series): return pd.Series(np.ones_like(arr.values))
            return np.ones_like(arr)
        def AD(self, high, low, close, volume):
            return np.ones_like(close)

    sys.modules["talib"] = MockTalib()
    sys.modules["talib.abstract"] = MockTalib()


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
