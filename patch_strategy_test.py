import sys
import mock

mock_talib = mock.MagicMock()
sys.modules['talib'] = mock_talib
sys.modules['talib.abstract'] = mock_talib.abstract
