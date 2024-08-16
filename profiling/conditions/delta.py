from profiling.profiler import Profile


class DeltaCondition(Profile):

    def __init__(self, tick_size, value_area_pct, delta_threshold):
        super().__init__(tick_size, value_area_pct)
        self.delta_threshold = delta_threshold

    def check(self, trade):
        self.process_trade(trade)
        delta = self.info['profiling'].get('delta', 0)

        if abs(delta) >= self.delta_threshold:
            print(f"delta condition met: delta: {delta}, Profile Info: {self.info}", '\n')
            self.reset()

    def reset(self):
        super().reset_info()
        print("Profile information has been reset.")
