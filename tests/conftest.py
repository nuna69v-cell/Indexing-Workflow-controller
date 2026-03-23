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
    import pandas as pd
    import numpy as np
    import sys
    from unittest.mock import MagicMock

    class TALibMock:
        def __init__(self):
            self.abstract = MagicMock()

        @property
        def __all__(self):
            return ["SMA", "RSI", "MACD", "BBANDS", "STOCH", "ATR", "NATR", "CCI", "WILLR", "ADX", "MOM", "ROC", "OBV", "HT_DCPERIOD", "MFI"]

        def _mock_array(self, *args, **kwargs):
            length = 100
            for arg in args:
                if hasattr(arg, '__len__') and not isinstance(arg, str):
                    length = len(arg)
                    break
            return pd.Series(np.ones(length))

        def _mock_array_3(self, *args, **kwargs):
            arr = self._mock_array(*args, **kwargs)
            return arr, arr, arr

        def _mock_array_2(self, *args, **kwargs):
            arr = self._mock_array(*args, **kwargs)
            return arr, arr

        def MACD(self, *args, **kwargs): return self._mock_array_3(*args, **kwargs)
        def BBANDS(self, *args, **kwargs): return self._mock_array_3(*args, **kwargs)
        def STOCH(self, *args, **kwargs): return self._mock_array_2(*args, **kwargs)

        def __getattr__(self, name):
            if name == 'abstract':
                return self.abstract
            if name in ['get_functions', 'get_function_groups']:
                return lambda: []
            return self._mock_array

    mock_talib = TALibMock()
    sys.modules["talib"] = mock_talib
    sys.modules["talib.abstract"] = mock_talib.abstract


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
