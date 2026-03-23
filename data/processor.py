import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp')
