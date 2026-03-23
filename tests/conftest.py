import os
import sys

import pytest

# Set testing environment variables before any application code is imported
os.environ["TESTING"] = "true"
os.environ["EA_API_KEY"] = "test_api_key_12345"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["JWT_SECRET"] = "test_jwt_secret"


class MockTalib:
    def SMA(self, *args, **kwargs):
        import numpy as np
        import pandas as pd

        length = len(args[0]) if args else 1
        return pd.Series(np.ones(length))

    def RSI(self, *args, **kwargs):
        import numpy as np
        import pandas as pd

        length = len(args[0]) if args else 1
        return pd.Series(np.ones(length))

    def MACD(self, *args, **kwargs):
        import numpy as np
        import pandas as pd

        length = len(args[0]) if args else 1
        return (
            pd.Series(np.ones(length)),
            pd.Series(np.ones(length)),
            pd.Series(np.ones(length)),
        )

    def BBANDS(self, *args, **kwargs):
        import numpy as np
        import pandas as pd

        length = len(args[0]) if args else 1
        return (
            pd.Series(np.ones(length)),
            pd.Series(np.ones(length)),
            pd.Series(np.ones(length)),
        )

    def STOCH(self, *args, **kwargs):
        import numpy as np
        import pandas as pd

        length = len(args[0]) if args else 1
        return pd.Series(np.ones(length)), pd.Series(np.ones(length))

    def get_functions(self):
        return []

    def get_function_groups(self):
        return {}

    def __getattr__(self, name):
        import numpy as np
        import pandas as pd

        def mock_func(*args, **kwargs):
            length = len(args[0]) if args else 100
            return pd.Series(np.ones(length))

        return mock_func


try:
    import talib  # noqa: F401
except ImportError:
    mock_talib = MockTalib()
    sys.modules["talib"] = mock_talib

    class MockTalibAbstract:
        TA_FUNC_FLAGS = {}
        TA_OUTPUT_FLAGS = {}
        TA_INPUT_FLAGS = {}
        TA_OPT_INPUT_FLAGS = {}

    sys.modules["talib.abstract"] = MockTalibAbstract()
    mock_talib.abstract = MockTalibAbstract()


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
