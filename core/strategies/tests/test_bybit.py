import unittest
from unittest.mock import Mock, patch
import os

from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    @patch.dict(
        os.environ,
        {"BYBIT_API_KEY": "test_api_key", "BYBIT_API_SECRET": "test_api_secret"},
    )
    @patch("pybit.unified_trading.HTTP.get_kline")
    def test_get_market_data(self, mock_get_kline):
        mock_get_kline.return_value = {"result": {"list": [1, 2, 3]}}

        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        self.assertTrue(mock_get_kline.called)
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch.dict(
        os.environ,
        {"BYBIT_API_KEY": "test_api_key", "BYBIT_API_SECRET": "test_api_secret"},
    )
    @patch("pybit.unified_trading.HTTP.place_order")
    def test_execute_order(self, mock_place_order):
        mock_place_order.return_value = {"result": {"orderId": "12345"}}

        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        self.assertTrue(mock_place_order.called)
        self.assertEqual(result, {"result": {"orderId": "12345"}})


if __name__ == "__main__":
    unittest.main()
