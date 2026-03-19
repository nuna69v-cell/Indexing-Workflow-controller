from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


@patch("api.utils.okta_auth.settings")
def test_predictions_requires_auth(mock_settings):
    mock_settings.OKTA_DOMAIN = "test.okta.com"
    with patch("os.getenv", return_value=""):
        response = client.post(
            "/api/v1/predictions",
            json={
                "historical_data": [
                    {"open": 1, "high": 2, "low": 1, "close": 1.5, "volume": 100}
                ]
            },
        )
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


@patch("api.utils.okta_auth.settings")
def test_scalping_requires_auth(mock_settings):
    mock_settings.OKTA_DOMAIN = "test.okta.com"
    with patch("os.getenv", return_value=""):
        response = client.post(
            "/api/v1/scalping/signals",
            json={
                "historical_data": [
                    {"open": 1, "high": 2, "low": 1, "close": 1.5, "volume": 100}
                ],
                "timeframe": "5m",
            },
        )
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
