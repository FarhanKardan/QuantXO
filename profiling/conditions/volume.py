import json
import numpy as np
from profiling.profiler import Profile
import os
import csv


def write_csv(data, filename="profiles.csv"):
    # os.remove("/Users/farhan/Desktop/QuantXO/profiles.csv")
    """
    Append a dictionary to a CSV file as a new row, converting numpy data types to native Python types.

    Args:
        data: Dictionary to be written to the file.
        filename: Name of the CSV file.
    """
    def convert_numpy(obj):
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj  # Return the object as-is if it's not a numpy type

    # Convert data to a format suitable for CSV
    flattened_data = {
        key: convert_numpy(value) for key, value in data.items()
    }

    # Open the CSV file in append mode and write the row
    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=flattened_data.keys())

        # Write the header only if the file is empty (first time writing)
        if f.tell() == 0:
            writer.writeheader()

        writer.writerow(flattened_data)

def write_json(data, filename="profiles.json"):
    os.remove("/Users/farhan/Desktop/QuantXO/profiles.json")
    with open(filename, "a") as f:  # Open in append mode
        json.dump(data, f, default=int)
        f.write("\n")


class VolumeCondition(Profile):
    """
    Condition to check if total volume exceeds a threshold.
    Inherits from Profile and uses its methods to process trades and check volume conditions.
    """

    def __init__(self, tick_size, value_area_pct, volume_threshold):
        super().__init__(tick_size, value_area_pct)
        self.volume_threshold = volume_threshold

    def check(self, trade):
        self.process_trade(trade)
        total_volume = self.info['profiling'].get('total_volume', 0)

        if total_volume >= self.volume_threshold:
            print(f"Volume condition met: Trade Size: {total_volume}, Profile Info: {self.info}")
            write_csv(self.info)
            self.reset()

    def reset(self):
        super().reset_info()
        # print("Profile information has been reset.")
