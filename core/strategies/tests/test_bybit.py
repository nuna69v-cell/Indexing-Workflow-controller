import unittest
import os
from unittest.mock import Mock, patch

import utils.config
from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    def setUp(self):
        # Set dummy API keys for testing
        utils.config.BYBIT_API_KEY = "test_api_key"
        utils.config.BYBIT_SECRET = "test_api_secret"

    @patch.dict(os.environ, {"BYBIT_API_KEY": "test", "BYBIT_API_SECRET": "test"})
    @patch("pybit.unified_trading.HTTP.get_kline")
    def test_get_market_data(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_get.return_value = {"result": {"list": [1, 2, 3]}}


        # Initialize the API and call the method
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert that the correct URL was called
        self.assertTrue(mock_get.called)
        pass

        # Assert that the response is handled correctly
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch.dict(os.environ, {"BYBIT_API_KEY": "test", "BYBIT_API_SECRET": "test"})
    @patch("pybit.unified_trading.HTTP.place_order")
    def test_execute_order(self, mock_post):
        # Mock the API response
        mock_response = Mock()
        mock_post.return_value = {"result": {"orderId": "12345"}}


        # Initialize the API and call the method
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert that the correct URL was called
        self.assertTrue(mock_post.called)
        pass

        # Assert that the response is handled correctly
        self.assertEqual(result, {"result": {"orderId": "12345"}})


if __name__ == "__main__":
    unittest.main()
