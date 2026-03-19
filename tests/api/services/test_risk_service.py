import pytest
from api.services.risk_service import RiskService
from api.models.schemas import OrderRequest, OrderType

@pytest.mark.asyncio
async def test_check_order_risk_approved():
    """Test check_order_risk when the order size is within limits."""
    service = RiskService()
    # By default, max_position_size is 0.1
    order_request = OrderRequest(
        symbol="XAUUSD",
        order_type=OrderType.BUY,
        quantity=0.05
    )
    result = await service.check_order_risk(order_request)
    assert result["approved"] is True
    assert result["reason"] == ""

@pytest.mark.asyncio
async def test_check_order_risk_rejected():
    """Test check_order_risk when the order size exceeds limits."""
    service = RiskService()
    # By default, max_position_size is 0.1
    order_request = OrderRequest(
        symbol="XAUUSD",
        order_type=OrderType.BUY,
        quantity=0.2
    )
    result = await service.check_order_risk(order_request)
    assert result["approved"] is False
    assert result["reason"] == "Position size too large"

@pytest.mark.asyncio
async def test_check_order_risk_exact_limit():
    """Test check_order_risk when the order size is exactly the limit."""
    service = RiskService()
    # By default, max_position_size is 0.1
    order_request = OrderRequest(
        symbol="XAUUSD",
        order_type=OrderType.BUY,
        quantity=0.1
    )
    result = await service.check_order_risk(order_request)
    assert result["approved"] is True
    assert result["reason"] == ""
