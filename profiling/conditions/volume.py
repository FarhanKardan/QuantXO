import json
import numpy as np
from profiling.profiler import Profile
from profiling.utils.csv_writer import CSVWriter  # Import the CSVWriter class


class VolumeCondition(Profile):
    def __init__(self, tick_size, value_area_pct, volume_threshold, csv_file_path):
        super().__init__(tick_size, value_area_pct)
        self.volume_threshold = volume_threshold
        self.csv_file_path = csv_file_path
        self.csv_writer = CSVWriter(file_path=csv_file_path)  # Initialize CSVWriter instance

    def check(self, trade):
        self.process_trade(trade)
        total_volume = self.info['profiling']['total_volume']

        if total_volume >= self.volume_threshold:
            print(self.info)
            print(f"Volume condition met: Trade Size: {total_volume}, Profile Info: {self.info}")

            # Write the record to CSV using CSVWriter
            self.csv_writer.write_record(self.info)

            self.reset()

    def reset(self):
        super().reset_info()
