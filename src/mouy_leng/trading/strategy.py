from typing import Optional

import backtrader as bt


class RSIMACDStrategy(bt.Strategy):
    """
    A basic trading strategy using RSI and MACD indicators.
    """

    params = (
        ("rsi_period", 14),
        ("rsi_overbought", 70),
        ("rsi_oversold", 30),
        ("macd_fast", 12),
        ("macd_slow", 26),
        ("macd_signal", 9),
    )

    def __init__(self) -> None:
        """Initialize indicators."""
        self.rsi: Optional[bt.indicators.RSI] = bt.indicators.RSI(
            self.data.close, period=self.params.rsi_period
        )
        self.macd: Optional[bt.indicators.MACD] = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.macd_fast,
            period_me2=self.params.macd_slow,
            period_signal=self.params.macd_signal,
        )

    def next(self) -> None:
        """Core strategy logic executed on each bar."""
        if not self.position:
            # Buy condition: RSI oversold AND MACD line crosses above Signal line
            if (
                self.rsi
                and self.macd
                and self.rsi[0] < self.params.rsi_oversold
                and self.macd.macd[0] > self.macd.signal[0]
            ):
                self.buy()
        else:
            # Sell condition: RSI overbought OR MACD line crosses below Signal line
            if (
                self.rsi
                and self.macd
                and (
                    self.rsi[0] > self.params.rsi_overbought
                    or self.macd.macd[0] < self.macd.signal[0]
                )
            ):
                self.sell()
