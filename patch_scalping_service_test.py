import sys
import mock
import numpy as np

mock_talib = mock.MagicMock()
mock_talib.RSI.return_value = np.random.rand(100)
mock_talib.MACD.return_value = (np.random.rand(100), np.random.rand(100), np.random.rand(100))
mock_talib.SMA.return_value = np.random.rand(100)
mock_talib.EMA.return_value = np.random.rand(100)
mock_talib.BBANDS.return_value = (np.random.rand(100), np.random.rand(100), np.random.rand(100))
mock_talib.ATR.return_value = np.random.rand(100)
mock_talib.ADX.return_value = np.random.rand(100)
mock_talib.STOCH.return_value = (np.random.rand(100), np.random.rand(100))
mock_talib.STOCHF.return_value = (np.random.rand(100), np.random.rand(100))
mock_talib.WILLR.return_value = np.random.rand(100)
mock_talib.CCI.return_value = np.random.rand(100)
mock_talib.MOM.return_value = np.random.rand(100)
mock_talib.ROC.return_value = np.random.rand(100)

sys.modules['talib'] = mock_talib
