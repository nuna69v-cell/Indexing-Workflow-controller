import backtrader as bt
import numpy as np
import pandas as pd
import pytest

from src.mouy_leng.trading.backtest import run_backtest
from src.mouy_leng.trading.strategy import RSIMACDStrategy


@pytest.fixture
def mock_data(tmp_path):
    """Generate dummy trading data for backtesting."""
    dates = pd.date_range("2023-01-01", periods=100)

    # Create an artificial downtrend then uptrend to trigger buy/sell
    prices = np.concatenate(
        [np.linspace(100, 50, 50), np.linspace(50, 150, 50)]  # Downtrend  # Uptrend
    )

    df = pd.DataFrame(
        {
            "Open": prices,
            "High": prices * 1.05,
            "Low": prices * 0.95,
            "Close": prices,
            "Volume": np.random.randint(1000, 10000, 100),
        },
        index=dates,
    )

    # Save to a temporary file
    file_path = tmp_path / "test_data.csv"
    df.to_csv(file_path, index_label="Date")

    return str(file_path)


def test_strategy_initialization():
    """Test that the strategy initializes correctly with its params."""
    cerebro = bt.Cerebro()
    cerebro.addstrategy(RSIMACDStrategy)

    # Use random walk data to avoid zero division in RSI
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=100)
    prices = 100 + np.random.randn(100).cumsum()
    df = pd.DataFrame(
        {
            "Open": prices,
            "High": prices + 2,
            "Low": prices - 2,
            "Close": prices,
            "Volume": np.random.randint(1000, 10000, 100),
        },
        index=dates,
    )

    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    strategy = cerebro.run()[0]
    assert strategy.params.rsi_period == 14
    assert strategy.params.macd_fast == 12


def test_run_backtest(mock_data):
    """Test the full backtesting function."""
    initial_cash = 10000.0
    cerebro = run_backtest(mock_data, cash=initial_cash)

    assert cerebro is not None
    assert (
        cerebro.broker.getvalue() != initial_cash
    )  # Should have traded or lost value due to commissions
