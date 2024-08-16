from collections import deque
from datetime import datetime, timedelta


class Candle:
    def __init__(self, open_price, high_price, low_price, close_price, volume, start_time, end_time):
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return (f"Candle(Open: {self.open_price}, High: {self.high_price}, "
                f"Low: {self.low_price}, Close: {self.close_price}, "
                f"Volume: {self.volume}, Start: {self.start_time}, End: {self.end_time})")


class CandleGenerator:
    def __init__(self, interval_seconds):
        self.interval_seconds = interval_seconds
        self.current_candle = None
        self.candles = deque()

    def _create_new_candle(self, price, volume, timestamp):
        start_time = timestamp
        end_time = start_time + timedelta(seconds=self.interval_seconds)
        self.current_candle = Candle(
            open_price=price,
            high_price=price,
            low_price=price,
            close_price=price,
            volume=volume,
            start_time=start_time,
            end_time=end_time
        )

    def process_tick(self, price, volume, timestamp):
        timestamp = datetime.fromtimestamp(timestamp)

        if self.current_candle is None:
            # Start the first candle
            self._create_new_candle(price, volume, timestamp)
        elif timestamp >= self.current_candle.end_time:
            # Close the current candle and start a new one
            self.candles.append(self.current_candle)
            self._create_new_candle(price, volume, timestamp)
        else:
            # Update the current candle
            self.current_candle.high_price = max(self.current_candle.high_price, price)
            self.current_candle.low_price = min(self.current_candle.low_price, price)
            self.current_candle.close_price = price
            self.current_candle.volume += volume

    def get_completed_candles(self):
        while len(self.candles) > 0:
            yield self.candles.popleft()

    def close_current_candle(self):
        if self.current_candle:
            self.candles.append(self.current_candle)
            self.current_candle = None
