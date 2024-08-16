from profiling.profiler import Profile
import time
import datetime

class DurationCondition(Profile):
    """
    Condition to check if the duration of the profile exceeds a threshold.
    Inherits from Profile and uses its methods to process trades and check duration conditions.
    """

    def __init__(self, tick_size, value_area_pct, duration_threshold):
        super().__init__(tick_size, value_area_pct)
        self.duration_threshold = duration_threshold

    def check(self, trade):
        self.process_trade(trade)

        duration_seconds = self.info['last_trade_ts'] - self.info['first_trade_ts']
        # print(">>>>>", duration_seconds, self.info)

        if duration_seconds >= self.duration_threshold:
            print(f"Duration condition met: Duration: {duration_seconds:.2f} seconds, Profile Info: {self.info}")
            self.reset()

    def reset(self):
        """
        Reset the profile information and update duration.
        """
        super().reset_info()
        print("Profile information has been reset.")
