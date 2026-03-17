import os

with open("core/strategies/tests/test_bybit.py", "r") as f:
    content = f.read()

content = content.replace("import unittest", "import unittest\nimport os")

content = content.replace("@patch(\"requests.post\")\n    def test_execute_order(self, mock_post):", "@patch.dict(os.environ, {\"BYBIT_API_KEY\": \"test\", \"BYBIT_API_SECRET\": \"test\"})\n    @patch(\"pybit.unified_trading.HTTP.place_order\")\n    def test_execute_order(self, mock_post):")

content = content.replace("@patch(\"requests.get\")\n    def test_get_market_data(self, mock_get):", "@patch.dict(os.environ, {\"BYBIT_API_KEY\": \"test\", \"BYBIT_API_SECRET\": \"test\"})\n    @patch(\"pybit.unified_trading.HTTP.get_kline\")\n    def test_get_market_data(self, mock_get):")


content = content.replace("mock_response.json.return_value = {\"result\": {\"orderId\": \"12345\"}}", "mock_post.return_value = {\"result\": {\"orderId\": \"12345\"}}")
content = content.replace("mock_post.return_value = mock_response", "")

content = content.replace("mock_response.json.return_value = {\"result\": {\"list\": [1, 2, 3]}}", "mock_get.return_value = {\"result\": {\"list\": [1, 2, 3]}}")
content = content.replace("mock_get.return_value = mock_response", "")

with open("core/strategies/tests/test_bybit.py", "w") as f:
    f.write(content)
