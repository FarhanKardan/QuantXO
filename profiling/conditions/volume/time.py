from profiling.conditions.base import BaseCondition
from datetime import datetime


class ProfileTime(BaseCondition):
    def __init__(self, tick_size, value_area_pct, duration):
        super().__init__(tick_size, value_area_pct)

        self.last_reset_time = 0
        self.duration = duration

    def trade(self, t):
        # FIX ME the time must be in another thread, this blocks until we have trade data
        time = datetime.fromtimestamp(t.timestamp / 1000)
        if self.last_reset_time == 0:
            self.last_reset_time = time
        if (time - self.last_reset_time).seconds > self.duration:
            self.reset()
            self.last_reset_time = time

        # update profile
        self.profile.update_trade(t)


