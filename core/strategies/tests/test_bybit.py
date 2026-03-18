import os
import unittest
from unittest.mock import Mock, patch

from core.execution.bybit import BybitAPI


class TestBybitAPI(unittest.TestCase):

    def setUp(self):
        # Set dummy API keys for testing
        os.environ["BYBIT_API_KEY"] = "test_api_key"
        os.environ["BYBIT_API_SECRET"] = "test_api_secret"

    @patch("core.execution.bybit.HTTP")
    def test_get_market_data(self, mock_http):
        # Mock the API response
        mock_session = Mock()
        mock_session.get_kline.return_value = {"result": {"list": [1, 2, 3]}}
        mock_http.return_value = mock_session

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        data = bybit_api.get_market_data("BTCUSDT", "1")

        # Assert that the correct URL was called
        self.assertTrue(mock_session.get_kline.called)

        # Assert that the response is handled correctly
        self.assertEqual(data, {"result": {"list": [1, 2, 3]}})

    @patch("core.execution.bybit.HTTP")
    def test_execute_order(self, mock_http):
        # Mock the API response
        mock_session = Mock()
        mock_session.place_order.return_value = {"result": {"orderId": "12345"}}
        mock_http.return_value = mock_session

        # Initialize the API and call the method
        bybit_api = BybitAPI()
        result = bybit_api.execute_order("BTCUSDT", "Buy", "Market", 0.01)

        # Assert that the correct URL was called
        self.assertTrue(mock_session.place_order.called)

        # Assert that the response is handled correctly
        self.assertEqual(result, {"result": {"orderId": "12345"}})


if __name__ == "__main__":
    unittest.main()
