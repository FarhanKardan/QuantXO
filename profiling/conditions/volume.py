from profiling.profiler import Profile
import csv
import json
import numpy as np

def write_json(data, filename="profiles.json"):
    """
    Writes a dictionary to a JSON file, converting numpy data types to native Python types.

    Args:
        data: Dictionary to be written to the file.
        filename: Name of the JSON file.
    """
    def convert_numpy(obj):
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        if isinstance(obj, (np.float64, np.float32)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert numpy arrays to lists
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with open(filename, "w") as f:
        json.dump(data, f, indent=4, default=convert_numpy)



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
            write_json(self.info)
            self.reset()

    def reset(self):
        super().reset_info()
        print("Profile information has been reset.")
