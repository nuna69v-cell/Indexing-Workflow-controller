import pytest
from datetime import datetime
from api.services.trading_service import TradingService
from api.models.schemas import SignalType

@pytest.mark.asyncio
async def test_get_active_signals_no_symbol():
    """Test that get_active_signals returns the mock signal when no symbol is provided."""
    service = TradingService()
    signals = await service.get_active_signals()

    assert len(signals) == 1
    assert signals[0].symbol == "BTCUSDT"
    assert signals[0].signal_type == SignalType.LONG
    assert signals[0].entry_price == 50000.0

@pytest.mark.asyncio
async def test_get_active_signals_with_matching_symbol():
    """Test that get_active_signals returns the mock signal when the correct symbol is provided."""
    service = TradingService()
    signals = await service.get_active_signals(symbol="BTCUSDT")

    assert len(signals) == 1
    assert signals[0].symbol == "BTCUSDT"

@pytest.mark.asyncio
async def test_get_active_signals_empty():
    """Test that get_active_signals returns an empty list when an unknown symbol is provided."""
    service = TradingService()
    signals = await service.get_active_signals(symbol="ETHUSDT")

    assert isinstance(signals, list)
    assert len(signals) == 0
