import sys  # noqa: E402
from unittest.mock import MagicMock  # noqa: E402

# Mock third-party dependencies required for tests
for mod in ['backtrader', 'fastapi', 'fastapi.testclient', 'pydantic_settings', 'joblib', 'aiohttp', 'pandas', 'numpy']:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

from unittest.mock import AsyncMock, MagicMock, patch  # noqa: E402

import pytest  # noqa: E402

import core.data_sources.fxcm_forexconnect_provider as provider_module  # noqa: E402

# Create a mock for the 'fx' module and add it to the provider module
# so that the test can find it.
mock_fx = MagicMock()
provider_module.fx = mock_fx

from core.data_sources.fxcm_forexconnect_provider import (  # noqa: E402  # noqa: E402  # noqa: E402
    FXCMForexConnectProvider,
)


@pytest.mark.asyncio
@patch("core.data_sources.fxcm_forexconnect_provider.FOREXCONNECT_AVAILABLE", True)
@patch("core.data_sources.fxcm_forexconnect_provider.aiohttp.ClientSession")
async def test_find_best_server(mock_session):
    # Mock the latency measurements
    async def mock_measure_latency(session, url):
        if "fxcorporate" in url:
            return 0.1
        elif "fxcm.com" in url:
            return 0.2
        else:
            return float("inf")

    # Configure the mock session
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock()

    # Create an instance of the provider
    config = {
        "username": "testuser",
        "password": "testpassword",
        "connection_type": "Demo",
        "auto_select_server": True,
    }
    provider = FXCMForexConnectProvider(config)
    provider._measure_latency = AsyncMock(side_effect=mock_measure_latency)

    # Run the test
    best_server = await provider.find_best_server()
    assert best_server == "http://www.fxcorporate.com/Hosts.jsp"


@pytest.mark.asyncio
@patch("core.data_sources.fxcm_forexconnect_provider.FOREXCONNECT_AVAILABLE", True)
async def test_connect_with_auto_select():
    # Mock the ForexConnect login

    # Create an instance of the provider
    config = {
        "username": "testuser",
        "password": "testpassword",
        "connection_type": "Demo",
        "auto_select_server": True,
    }
    provider = FXCMForexConnectProvider(config)

    # Mock the find_best_server method
    provider.find_best_server = AsyncMock(return_value="https://best.server.com")

    # Run the test
    await provider.connect()

    # Check that login was called with the best server
    provider.forex_connect.login.assert_called_with(
        user_id="testuser",
        password="testpassword",
        url="https://best.server.com",
        connection="Demo",
        session_id=None,
        pin=None,
    )
