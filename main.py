from log_handler.logger import Logger
from profiling.conditions.volume import VolumeCondition
from profiling.clusters.candles import CandleGenerator
from data_handler.data_reader.data_reader import DataReader
from datetime import datetime


class Trade:
    def __init__(self, price, side, size, timestamp):
        self.price = price
        self.side = side
        self.size = size
        self.timestamp = timestamp


if __name__ == "__main__":
    # set logger and data downloader
    logger_instance = Logger().get_logger()
    reader = DataReader(dir_path="/Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT")
    df = reader.daterange(datetime(2024, 8, 1), datetime(2024, 8, 3))
    df['size'] = df['price'] * df['size']
    # df = df[:19000]

    candle_generator = CandleGenerator(interval_seconds=60)

    profiler = VolumeCondition(
        value_area_pct=0.7,
        tick_size=100,
        volume_threshold=10_000_000)

    for i, row in df.iterrows():
        candle_generator.process_tick(price=row['price'], volume=row['size'], timestamp=row['timestamp'])
        trade = Trade(price=row['price'], side=row['side'], size=row['size'], timestamp=row['timestamp'])
        profiler.check(trade)
    candle_generator.convert_candle_into_csv()
