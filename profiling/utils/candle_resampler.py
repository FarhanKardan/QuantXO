import pandas as pd

class TickResampler:
    def __init__(self, df):
        """
        Initialize the TickResampler with tick data.

        Args:
            df (pd.DataFrame): DataFrame containing tick data with at least 'timestamp', 'price', and 'volume' columns.
        """
        # Check if 'timestamp' is already in datetime format, if not convert it
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Assuming timestamps are in seconds
        self.df = df.copy()
        self.df = self.df.sort_values('timestamp')
        self.df.set_index('timestamp', inplace=True)

    def resample_to_candles(self, timeframe='1T'):
        """
        Resample tick data into OHLC candles.

        Args:
            timeframe (str): Resample timeframe (e.g., '1T' for 1-minute candles, '5T' for 5-minute candles).

        Returns:
            pd.DataFrame: DataFrame containing OHLCV data.
        """
        # Define the aggregation dictionary
        ohlc_dict = {
            'price': 'ohlc',
            'size': 'sum'

        }

        # Resample the DataFrame to the specified timeframe
        resampled = self.df.resample(timeframe).apply(ohlc_dict)

        # Flatten the multi-level column structure resulting from the 'ohlc' aggregation
        resampled.columns = ['open', 'high', 'low', 'close', 'volume']

        # Drop periods with NaNs (no ticks during the period)
        resampled.dropna(inplace=True)

        return resampled

    def get_original_data(self):
        """
        Retrieve the original tick data.

        Returns:
            pd.DataFrame: Original tick data.
        """
        return self.df
