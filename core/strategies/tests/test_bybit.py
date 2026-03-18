import unittest
from unittest.mock import Mock, patch

import utils.config
from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    def setUp(self):
        # Set dummy API keys for testing
        utils.config.BYBIT_API_KEY = "test_api_key"
        utils.config.BYBIT_SECRET = "test_api_secret"

    @patch("core.execution.bybit.HTTP.get_kline")
    @patch(
        "os.environ.get",
        side_effect=lambda k: (
            "mock_key" if k in ["BYBIT_API_KEY", "BYBIT_API_SECRET"] else None
        ),
    )
    def test_get_market_data(self, mock_env_get, mock_get_kline):
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {"result": {"list": [1, 2, 3]}}
        mock_get_kline.return_value = {"result": {"list": [1, 2, 3]}}

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert that the correct URL was called
        self.assertTrue(mock_get_kline.called)

        # Assert that the response is handled correctly
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch("core.execution.bybit.HTTP.place_order")
    @patch(
        "os.environ.get",
        side_effect=lambda k: (
            "mock_key" if k in ["BYBIT_API_KEY", "BYBIT_API_SECRET"] else None
        ),
    )
    def test_execute_order(self, mock_env_get, mock_place_order):
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {"result": {"orderId": "12345"}}
        mock_place_order.return_value = {"result": {"orderId": "12345"}}

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert that the correct URL was called
        self.assertTrue(mock_place_order.called)

        # Assert that the response is handled correctly
        self.assertEqual(result, {"result": {"orderId": "12345"}})


if __name__ == "__main__":
    unittest.main()
