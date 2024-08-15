from profiling.conditions.base import BaseCondition


class ProfileDelta(BaseCondition):
    def __init__(self, tick_size, value_area_pct, positive_delta, negative_delta):
        # calling super class init
        super().__init__(tick_size, value_area_pct)

        self.positive_delta = positive_delta
        self.negative_delta = negative_delta

    def trade(self, t):
        delta = self.profile.volume_profile.info['delta']
        if delta >= self.positive_delta or delta <= self.negative_delta:
            self.reset()

        self.profile.update_trade(t)



