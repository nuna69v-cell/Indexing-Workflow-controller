import unittest
from unittest.mock import Mock, patch
import os

from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    def setUp(self):
        # Set dummy API keys for testing in the environment, since BybitAPI reads os.environ
        os.environ["BYBIT_API_KEY"] = "test_api_key"
        os.environ["BYBIT_API_SECRET"] = "test_api_secret"

    def tearDown(self):
        # Clean up the environment
        if "BYBIT_API_KEY" in os.environ:
            del os.environ["BYBIT_API_KEY"]
        if "BYBIT_API_SECRET" in os.environ:
            del os.environ["BYBIT_API_SECRET"]

    @patch("core.execution.bybit.HTTP")
    def test_get_market_data(self, mock_http):
        # Mock the API response
        mock_instance = Mock()
        mock_instance.get_kline.return_value = {"result": {"list": [1, 2, 3]}}
        mock_http.return_value = mock_instance

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert that the correct method was called
        mock_instance.get_kline.assert_called_once_with(
            category="spot", symbol="BTCUSDT", interval="1", limit=200
        )

        # Assert that the response is handled correctly
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch("core.execution.bybit.HTTP")
    def test_execute_order(self, mock_http):
        # Mock the API response
        mock_instance = Mock()
        mock_instance.place_order.return_value = {"result": {"orderId": "12345"}}
        mock_http.return_value = mock_instance

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert that the correct method was called
        mock_instance.place_order.assert_called_once_with(
            category="spot", symbol="BTCUSDT", side="Buy", orderType="Market", qty="0.01"
        )

        # Assert that the response is handled correctly
        self.assertEqual(result, {"result": {"orderId": "12345"}})


if __name__ == "__main__":
    unittest.main()
