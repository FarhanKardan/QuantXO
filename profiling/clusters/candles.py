from collections import deque
from datetime import datetime, timedelta
import pandas as pd


class CandleGenerator:
    def __init__(self, interval_seconds):
        self.interval_seconds = interval_seconds
        self.current_candle = None
        self.candles = deque()

    def process_tick(self, price, volume, timestamp):
        timestamp = datetime.fromtimestamp(timestamp)

        if self.current_candle is None:
            # Start the first candle
            start_time = timestamp
            end_time = start_time + timedelta(seconds=self.interval_seconds)
            self.current_candle = {
                "open_price": price,
                "high_price": price,
                "low_price": price,
                "close_price": price,
                "volume": volume,
                "start_time": start_time,
                "end_time": end_time
            }
        elif timestamp >= self.current_candle["end_time"]:
            # Close the current candle and start a new one
            self.candles.append(self.current_candle)
            start_time = timestamp
            end_time = start_time + timedelta(seconds=self.interval_seconds)
            self.current_candle = {
                "open_price": price,
                "high_price": price,
                "low_price": price,
                "close_price": price,
                "volume": volume,
                "start_time": start_time,
                "end_time": end_time
            }
        else:
            candle = self.current_candle
            candle["high_price"] = max(candle["high_price"], price)
            candle["low_price"] = min(candle["low_price"], price)
            candle["close_price"] = price
            candle["volume"] += volume

    def get_completed_candles(self):
        while self.candles:
            yield self.candles.popleft()

    def close_current_candle(self):
        if self.current_candle:
            self.candles.append(self.current_candle)
            self.current_candle = None

    def convert_candles_to_dataframe(self):
        # Convert deque of candle dictionaries to a Pandas DataFrame
        df = pd.DataFrame(self.candles)
        return df
