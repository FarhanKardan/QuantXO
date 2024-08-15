from log_handler.logger import Logger
import pandas as pd
from profiling.conditional.volume.volume import ProfileVolume
from queue import Queue
from profiling.base import Profile


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
    df = df[:1000]

    q = Queue()
    profiler = Profile(
        value_area_pct=0.7,
        tick_size=20,
        queue=q,
    )

    for _, row in df.iterrows():
        trade = Trade(price=row['price'], side=row['side'], size=row['size'], timestamp=row['timestamp'])
        profiler.update_trade(trade)
        print(profiler.info, '\n')
        break
