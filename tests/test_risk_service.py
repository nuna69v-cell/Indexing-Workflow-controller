import pytest
from api.services.risk_service import RiskService
from api.models.schemas import OrderRequest, OrderType

@pytest.fixture
def risk_service():
    return RiskService()

@pytest.mark.asyncio
async def test_assess_signal_risk(risk_service):
    # Test the basic functionality (currently returns a hardcoded 0.5)
    mock_signal = {"symbol": "XAUUSD", "type": "long"}
    result = await risk_service.assess_signal_risk(mock_signal)

    assert isinstance(result, float)
    assert result == 0.5

@pytest.mark.asyncio
async def test_check_order_risk_approved(risk_service):
    order = OrderRequest(
        symbol="XAUUSD",
        order_type=OrderType.BUY,
        quantity=0.05
    )

    result = await risk_service.check_order_risk(order)

    assert result["approved"] is True
    assert result["reason"] == ""

@pytest.mark.asyncio
async def test_check_order_risk_rejected(risk_service):
    order = OrderRequest(
        symbol="XAUUSD",
        order_type=OrderType.BUY,
        quantity=0.2
    )

    result = await risk_service.check_order_risk(order)

    assert result["approved"] is False
    assert result["reason"] == "Position size too large"

@pytest.mark.asyncio
async def test_check_order_risk_boundary(risk_service):
    order = OrderRequest(
        symbol="XAUUSD",
        order_type=OrderType.SELL,
        quantity=0.1
    )

    result = await risk_service.check_order_risk(order)

    assert result["approved"] is True
    assert result["reason"] == ""
