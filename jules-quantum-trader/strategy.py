import pandas as pd

class MovingAverageCrossover:
    """
    A simple Moving Average Crossover Strategy.
    Buys when the fast MA crosses above the slow MA.
    Sells when the fast MA crosses below the slow MA.
    """
    def __init__(self, fast_period=10, slow_period=50):
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        Analyzes the latest data and returns a trading signal.
        Expects a DataFrame with 'close' prices.
        Returns: 'BUY', 'SELL', or 'HOLD'
        """
        if len(data) < self.slow_period:
            return 'HOLD'

        # Calculate Moving Averages
        data['fast_ma'] = data['close'].rolling(window=self.fast_period).mean()
        data['slow_ma'] = data['close'].rolling(window=self.slow_period).mean()

        # Get latest two rows to check for crossover
        last_row = data.iloc[-1]
        prev_row = data.iloc[-2]

        if prev_row['fast_ma'] <= prev_row['slow_ma'] and last_row['fast_ma'] > last_row['slow_ma']:
            return 'BUY'
        elif prev_row['fast_ma'] >= prev_row['slow_ma'] and last_row['fast_ma'] < last_row['slow_ma']:
            return 'SELL'

        return 'HOLD'
