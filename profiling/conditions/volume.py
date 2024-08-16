from profiling.profiler import Profile


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
            self.reset()

    def reset(self):
        super().reset_info()
        print("Profile information has been reset.")
