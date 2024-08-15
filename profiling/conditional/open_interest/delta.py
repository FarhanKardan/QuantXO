from core.profile.conditional.base import BaseCondition


class OpenInterestDelta(BaseCondition):
    def __init__(self, exchange, symbol, tick_size, value_area_pct, positive_delta, negative_delta):
        super().__init__(exchange, symbol, tick_size, value_area_pct)

        self.positive_delta = positive_delta
        self.negative_delta = negative_delta

    def trade(self, t):
        self.profile.update_trade(t)

    def instrument(self, i):
        delta = self.profile.open_interest_profile.info['delta']
        if delta > 0:
            if delta >= self.positive_delta:
                self.reset()
        else:
            if delta <= self.negative_delta:
                self.reset()

        self.profile.update_instrument(i)

    def liquidation(self, liq):
        self.profile.update_liquidation(liq)

    def orderbook(self, o):
        return

