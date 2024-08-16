from log_handler.logger import Logger
import pandas as pd
from profiling.conditions.volume import VolumeCondition
from profiling.conditions.delta import DeltaCondition
from profiling.conditions.time import DurationCondition
from queue import Queue
from profiling.profiler import Profile


class Trade:
    def __init__(self, price, side, size, timestamp):
        self.price = price
        self.side = side
        self.size = size
        self.timestamp = timestamp


if __name__ == "__main__":
    # set logger and data downloader
    logger_instance = Logger().get_logger()
    # fetcher = BybitTickFetcher(logger=logger_instance).run(start_date=datetime(2024, 8, 9), end_date=datetime(2024, 8, 12 ))
    df = pd.read_csv("/Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT2024-08-09.csv.gz", compression="gzip")
    df['size'] = df['price'] * df['size']
    df = df[:1007]

    profiler = DurationCondition(
        value_area_pct=0.7,
        tick_size=100,
        duration_threshold=30,
    )

    for i, row in df.iterrows():
        trade = Trade(price=row['price'], side=row['side'], size=row['size'], timestamp=row['timestamp'])
        profiler.check(trade)
        # if profiler.info['profiling']['total_volume'] > 5000000:
        #     print("Each tick update", profiler.info,'\n')
        #     profiler.reset_info()

