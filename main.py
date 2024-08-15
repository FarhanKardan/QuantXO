from log_handler.logger import Logger
import pandas as pd
from profiling.base import Profile
from profiling.conditional.volume.volume import ProfileVolume
from queue import Queue

if __name__ == "__main__":
    # set logger and data downloader
    logger_instance = Logger().get_logger()
    # fetcher = BybitTickFetcher(logger=logger_instance).run(start_date=datetime(2024, 8, 9), end_date=datetime(2024, 8, 12 ))
    df = pd.read_csv("/Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT2024-08-09.csv.gz", compression="gzip")
    df = df[:1000]

    q = Queue()

    profiler = ProfileVolume(
        symbol="BTCUSDT",
        exchange="test",
        value_area_pct=0.7,
        tick_size=20,
        volume=5000
    )

    for _, row in df.iterrows():
        profiler.trade(row)
        # print('\n')

