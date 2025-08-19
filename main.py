from profiling.conditions.volume import VolumeCondition
from profiling.utils.types import Trade
from data_feeder.historical_data_reader import DataReader
import time


def main():
    """Main function to orchestrate the entire workflow"""
    # Initialize data reader
    data_reader = DataReader()
    
    s = time.time()
    profiler = VolumeCondition(
        value_area_pct=0.7,
        tick_size=100,
        volume_threshold=500000,
        csv_file_path="volume_profile.csv"
    )
    
    # Process ticks using iterate_ticks
    for tick_data in data_reader.iterate_ticks("2024-05-01", "2024-05-01"):
        trade = Trade(price=tick_data.price, side=tick_data.side, size=tick_data.size, timestamp=tick_data.timestamp)
        profiler.check(trade)
    
    print(time.time() - s)


if __name__ == "__main__":
    main()

