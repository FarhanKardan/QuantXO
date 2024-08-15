import pandas as pd
from datetime import datetime, timedelta
import os


def create_dataframe(klines):
    df = pd.DataFrame(klines)
    df.columns = [
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ]
    df['Date'] = pd.to_datetime(df['Open time'], unit='ms')
    df.set_index('Date', inplace=True)
    return df



