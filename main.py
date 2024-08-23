from log_handler.logger import Logger
from profiling.conditions.volume import VolumeCondition
from profiling.clusters.candles import CandleGenerator
from data_handler.data_reader.data_reader import DataReader
from datetime import datetime
import time
from profiling.utils.types import Trade
from profiling.utils.candle_resampler import TickResampler



if __name__ == "__main__":

    # set logger and data downloader
    logger_instance = Logger().get_logger()
    reader = DataReader(dir_path="/Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT")
    df = reader.daterange(datetime(2024, 8, 1), datetime(2024, 8, 3))
    df['size'] = df['price'] * df['size']
    print(df)
    # df = df[:100000]

    # Creating Candles
    candle_df = TickResampler(df).resample_to_candles(timeframe="1min")
    candle_df.to_csv("candle_1m.csv")
    print(candle_df)

    s = time.time()
    # profiler = VolumeCondition(
    #     value_area_pct=0.7,
    #     tick_size=100,
    #     volume_threshold=10_000_000,
    #     csv_file_path="volume_profile.csv")
    #
    # for i, row in df.iterrows():
    #     trade = Trade(price=row['price'], side=row['side'], size=row['size'], timestamp=row['timestamp'])
    #     profiler.check(trade)
    print(time.time() - s)

