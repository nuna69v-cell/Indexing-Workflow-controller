"""
Technical Feature Engineering for GenX FX Trading System
Generates technical indicators and features for ML models
"""

import os
import sys
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.technical_indicators import TechnicalIndicators


class TechnicalFeatureEngine:
    """
    A feature engineering engine for generating technical indicators.

    This class takes a DataFrame of OHLCV data and enriches it with a wide
    array of technical analysis features, including price-based features,
    moving averages, and various indicators for momentum, volatility, and volume.

    Attributes:
        tech_indicators (TechnicalIndicators): An instance of the technical indicators utility class.
        feature_columns (List[str]): A list to store the names of the generated feature columns.
    """

    def __init__(self):
        """Initializes the TechnicalFeatureEngine."""
        self.tech_indicators = TechnicalIndicators()
        self.feature_columns = []

    def generate_features(
        self, df: pd.DataFrame, symbol: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Generates a comprehensive set of technical features from OHLCV data.

        Args:
            df (pd.DataFrame): A DataFrame with 'Open', 'High', 'Low', 'Close',
                               and optionally 'Volume' columns.
            symbol (Optional[str]): The trading symbol (currently unused, but
                                    available for future symbol-specific logic).

        Returns:
            pd.DataFrame: The original DataFrame enriched with technical feature columns.
        """
        if df.empty or len(df) < 50:
            return df

        # Make a copy to avoid modifying original
        features_df = df.copy()

        try:
            # Price-based features
            features_df = self._add_price_features(features_df)

            # Moving averages
            features_df = self._add_moving_averages(features_df)

            # Momentum indicators
            features_df = self._add_momentum_indicators(features_df)

            # Volatility indicators
            features_df = self._add_volatility_indicators(features_df)

            # Volume indicators (if volume available)
            if "Volume" in features_df.columns:
                features_df = self._add_volume_indicators(features_df)

            # Pattern features
            features_df = self._add_pattern_features(features_df)

            # Fill any NaN values
            features_df = features_df.bfill().ffill().fillna(0)

        except Exception as e:
            print(f"Warning: Error generating features: {e}")
            return df

        return features_df

    def _add_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds basic price-based features to the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added price features.
        """
        df["HL_pct"] = (df["High"] - df["Low"]) / df["Close"] * 100
        df["OC_pct"] = (df["Open"] - df["Close"]) / df["Close"] * 100
        df["price_change"] = df["Close"].pct_change()
        df["price_range"] = df["High"] - df["Low"]
        df["body_size"] = abs(df["Close"] - df["Open"])
        # ---
        # ⚡ Bolt Optimization: Vectorized row-wise min/max
        # Replacing df[["Open", "Close"]].max(axis=1) with np.maximum(Open.values, Close.values)
        # avoids costly index alignment and series overhead, resulting in a measurable speedup.
        # ---
        open_vals = df["Open"].values
        close_vals = df["Close"].values
        df["upper_shadow"] = df["High"].values - np.maximum(open_vals, close_vals)
        df["lower_shadow"] = np.minimum(open_vals, close_vals) - df["Low"].values

        return df

    def _add_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds moving average features to the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added moving average features.
        """
        periods = [5, 10, 20, 50, 100, 200]

        # ---
        # ⚡ Bolt Optimization: Vectorized SMA and EMA calculations
        # Using numpy convolution instead of Pandas rolling().mean() for faster
        # moving average feature generation.
        # ---
        close_vals = df["Close"].values

        for period in periods:
            if len(df) >= period:
                # SMA
                kernel = np.ones(period) / period
                sma_vals = np.convolve(close_vals, kernel, mode="valid")
                sma_full = np.full(len(df), np.nan)
                sma_full[period - 1 :] = sma_vals
                df[f"sma_{period}"] = sma_full

                # EMA (Still relying on Pandas EWM as it's optimized in Cython)
                df[f"ema_{period}"] = df["Close"].ewm(span=period).mean()

                # Price vs Averages (Vectorized)
                df[f"price_vs_sma_{period}"] = (
                    (close_vals - sma_full) / sma_full
                ) * 100
                df[f"price_vs_ema_{period}"] = (
                    (close_vals - df[f"ema_{period}"].values)
                    / df[f"ema_{period}"].values
                ) * 100

        # Moving average crossovers (Vectorized)
        if len(df) >= 50 and "sma_5" in df and "sma_20" in df and "sma_50" in df:
            df["sma_5_vs_20"] = (
                (df["sma_5"].values - df["sma_20"].values) / df["sma_20"].values * 100
            )
            df["sma_10_vs_50"] = (
                (df["sma_10"].values - df["sma_50"].values) / df["sma_50"].values * 100
            )

        return df

    def _add_momentum_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds momentum-based indicator features to the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added momentum features.
        """
        try:
            # The underlying `tech_indicators` utility has been updated.
            # We now rely on `tech_indicators.add_all_indicators()` directly
            # instead of individual methods. For now we will compute the
            # specific indicators locally or use Pandas as fallback since
            # the old individual methods (like .rsi) are no longer exposed.

            # We use `lower_df` to extract values directly, since `tech_indicators` expects
            # lowercase column names to calculate all of them.
            lower_df = df.copy()
            lower_df.columns = [c.lower() for c in lower_df.columns]
            df_with_inds = self.tech_indicators.add_all_indicators(lower_df)
            if "rsi" in df_with_inds.columns:
                df["rsi"] = df_with_inds["rsi"]

            if "macd" in df_with_inds.columns:
                df["macd"] = df_with_inds["macd"]
                df["macd_signal"] = df_with_inds["macd_signal"]
                df["macd_histogram"] = df_with_inds["macd_histogram"]

            if "stoch_k" in df_with_inds.columns:
                df["stoch_k"] = df_with_inds["stoch_k"]
                df["stoch_d"] = df_with_inds["stoch_d"]

            # ROC (Rate of Change)
            for period in [5, 10, 20]:
                if len(df) >= period:
                    df[f"roc_{period}"] = df["Close"].pct_change(periods=period) * 100

            # Williams %R
            if "williams_r" in df_with_inds.columns:
                df["williams_r"] = df_with_inds["williams_r"]

        except Exception as e:
            print(f"Warning: Error adding momentum indicators: {e}")

        return df

    def _add_volatility_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds volatility-based indicator features to the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added volatility features.
        """
        try:
            # Fetch indicators from the updated utility
            # Make sure column names are lowercase as expected by the utility
            lower_df = df.copy()
            lower_df.columns = [c.lower() for c in lower_df.columns]
            df_with_inds = self.tech_indicators.add_all_indicators(lower_df)

            # Bollinger Bands
            if "bb_upper" in df_with_inds.columns:
                df["bb_upper"] = df_with_inds["bb_upper"]
                df["bb_middle"] = df_with_inds["bb_middle"]
                df["bb_lower"] = df_with_inds["bb_lower"]
                df["bb_width"] = df_with_inds["bb_width"]
                df["bb_position"] = df_with_inds["bb_position"]

            # ATR
            if "atr" in df_with_inds.columns:
                df["atr"] = df_with_inds["atr"]
                df["atr_pct"] = df_with_inds["atr"] / df["Close"] * 100

            # Price volatility
            # ---
            # ⚡ Bolt Optimization: Vectorized rolling std
            # Replaces slow pd.Series.rolling().std() with vectorized variance formula
            # using numpy.convolve.
            # ---
            close_vals = df["Close"].values
            close_sq_vals = close_vals**2

            for period in [5, 10, 20]:
                if len(df) >= period:
                    s = np.convolve(close_vals, np.ones(period), mode="valid")
                    s2 = np.convolve(close_sq_vals, np.ones(period), mode="valid")
                    var = (s2 - (s**2 / period)) / (period - 1)

                    vol_vals = np.full(len(df), np.nan)
                    vol_vals[period - 1 :] = np.sqrt(np.maximum(var, 0))

                    df[f"volatility_{period}"] = vol_vals
                    df[f"volatility_pct_{period}"] = (vol_vals / close_vals) * 100

        except Exception as e:
            print(f"Warning: Error adding volatility indicators: {e}")

        return df

    def _add_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds volume-based indicator features to the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added volume features.
        """
        try:
            # Volume moving averages
            for period in [5, 10, 20]:
                if len(df) >= period:
                    df[f"volume_ma_{period}"] = (
                        df["Volume"].rolling(window=period).mean()
                    )
                    df[f"volume_ratio_{period}"] = (
                        df["Volume"] / df[f"volume_ma_{period}"]
                    )

            # Price-Volume features
            df["price_volume"] = df["Close"] * df["Volume"]
            df["volume_change"] = df["Volume"].pct_change()

        except Exception as e:
            print(f"Warning: Error adding volume indicators: {e}")

        return df

    def _add_pattern_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds candlestick and trend pattern features to the DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added pattern features.
        """
        try:
            # Simple candlestick pattern detection
            df["is_doji"] = (
                abs(df["Close"] - df["Open"]) / (df["High"] - df["Low"]) < 0.1
            ).astype(int)
            df["is_hammer"] = (
                (df["Close"] > df["Open"])
                & (df["lower_shadow"] > 2 * df["body_size"])
                & (df["upper_shadow"] < df["body_size"])
            ).astype(int)
            df["is_shooting_star"] = (
                (df["Close"] < df["Open"])
                & (df["upper_shadow"] > 2 * df["body_size"])
                & (df["lower_shadow"] < df["body_size"])
            ).astype(int)

            # Trend patterns
            df["higher_high"] = (df["High"] > df["High"].shift(1)).astype(int)
            df["lower_low"] = (df["Low"] < df["Low"].shift(1)).astype(int)
            df["higher_close"] = (df["Close"] > df["Close"].shift(1)).astype(int)

        except Exception as e:
            print(f"Warning: Error adding pattern features: {e}")

        return df

    def get_feature_importance(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculates basic feature importance based on correlation with price movement.

        Args:
            df (pd.DataFrame): A DataFrame containing features and a 'price_change' column.

        Returns:
            Dict[str, float]: A dictionary mapping feature names to their absolute
                              correlation with price change, sorted by importance.
        """
        if "price_change" not in df.columns:
            return {}

        try:
            # Get numeric columns only
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            feature_cols = [
                col
                for col in numeric_cols
                if col not in ["Open", "High", "Low", "Close", "Volume"]
            ]

            # Calculate correlation with price change
            correlations = {}
            for col in feature_cols:
                if col in df.columns and not df[col].isna().all():
                    corr = abs(df[col].corr(df["price_change"]))
                    if not np.isnan(corr):
                        correlations[col] = corr

            # Sort by importance
            sorted_features = dict(
                sorted(correlations.items(), key=lambda x: x[1], reverse=True)
            )
            return sorted_features

        except Exception as e:
            print(f"Warning: Error calculating feature importance: {e}")
            return {}

    def select_top_features(self, df: pd.DataFrame, n_features: int = 20) -> List[str]:
        """
        Selects the top N most important features based on correlation.

        Args:
            df (pd.DataFrame): The DataFrame with features.
            n_features (int): The number of top features to select.

        Returns:
            List[str]: A list of the names of the top N features.
        """
        importance = self.get_feature_importance(df)
        return list(importance.keys())[:n_features]
