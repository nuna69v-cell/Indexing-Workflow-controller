from typing import Optional

import backtrader as bt
import pandas as pd

from .strategy import RSIMACDStrategy


def run_backtest(data_file: str, cash: float = 10000.0) -> Optional[bt.Cerebro]:
    """
    Run a backtest using the given historical data file.

    Args:
        data_file (str): Path to a CSV file with columns: Date, Open, High, Low, Close, Volume
        cash (float): Initial capital for the backtest

    Returns:
        bt.Cerebro: The cerebro instance after the backtest run.
    """
    try:
        cerebro: bt.Cerebro = bt.Cerebro()

        # Load data
        df: pd.DataFrame = pd.read_csv(data_file, parse_dates=True, index_col="Date")
        data: bt.feeds.PandasData = bt.feeds.PandasData(dataname=df)

        cerebro.adddata(data)
        cerebro.addstrategy(RSIMACDStrategy)
        cerebro.broker.setcash(cash)
        cerebro.broker.setcommission(commission=0.001)  # 0.1% commission

        print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
        cerebro.run()
        print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

        return cerebro
    except Exception as e:
        print(f"Error during backtest: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    # run_backtest('historical_data.csv')
    pass
