import pytest
import pandas as pd
import numpy as np
from data.processor import clean_data


def test_clean_data_normal():
    raw_data = {
        "timestamp": [
            "2023-01-03 10:00:00",
            "2023-01-01 10:00:00",
            None,
            "2023-01-02 10:00:00",
        ],
        "value": [3.0, 1.0, 4.0, np.nan],
        "category": ["A", "B", "C", "D"],
    }
    df = pd.DataFrame(raw_data)

    cleaned_df = clean_data(df)

    # Should have 2 rows because 2 rows have NAs
    assert len(cleaned_df) == 2

    # Timestamp should be datetime
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["timestamp"])

    # Should be sorted
    timestamps = cleaned_df["timestamp"].tolist()
    assert timestamps[0] == pd.Timestamp("2023-01-01 10:00:00")
    assert timestamps[1] == pd.Timestamp("2023-01-03 10:00:00")

    # Values should match the sorted order
    values = cleaned_df["value"].tolist()
    assert values[0] == 1.0
    assert values[1] == 3.0


def test_clean_data_empty_df():
    df = pd.DataFrame(columns=["timestamp", "value"])
    cleaned_df = clean_data(df)

    assert len(cleaned_df) == 0
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["timestamp"])


def test_clean_data_missing_timestamp_column():
    df = pd.DataFrame({"value": [1.0, 2.0]})

    with pytest.raises(KeyError):
        clean_data(df)
