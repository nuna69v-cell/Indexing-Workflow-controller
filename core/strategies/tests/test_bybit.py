import os
import unittest
from unittest.mock import patch

import utils.config
from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    def setUp(self):
        # Set dummy API keys for testing
        os.environ["BYBIT_API_KEY"] = "test_api_key"
        os.environ["BYBIT_API_SECRET"] = "test_api_secret"
        utils.config.BYBIT_API_KEY = "test_api_key"
        utils.config.BYBIT_SECRET = "test_api_secret"

    @patch("core.execution.bybit.HTTP.get_kline")
    def test_get_market_data(self, mock_get_kline):
        # Mock the API response
        mock_get_kline.return_value = {"result": {"list": [1, 2, 3]}}

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert that the correct method was called
        self.assertTrue(mock_get_kline.called)

        # Assert that the response is handled correctly
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch("core.execution.bybit.HTTP.place_order")
    def test_execute_order(self, mock_place_order):
        # Mock the API response
        mock_place_order.return_value = {"result": {"orderId": "12345"}}

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert that the correct method was called
        self.assertTrue(mock_place_order.called)

        # Assert that the response is handled correctly
        self.assertEqual(result, {"result": {"orderId": "12345"}})


if __name__ == "__main__":
    unittest.main()
