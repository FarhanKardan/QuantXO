from core.profile.conditional.base import BaseCondition


class ProfileDelta(BaseCondition):
    def __init__(self, exchange, symbol, tick_size, value_area_pct, positive_delta, negative_delta):
        # calling super class init
        super().__init__(exchange, symbol, tick_size, value_area_pct)

        self.positive_delta = positive_delta
        self.negative_delta = negative_delta

    def trade(self, t):
        delta = self.profile.volume_profile.info['delta']
        if delta >= self.positive_delta or delta <= self.negative_delta:
            self.reset()

        self.profile.update_trade(t)

    def instrument(self, i):
        self.profile.update_instrument(i)

    def liquidation(self, liq):
        self.profile.update_liquidation(liq)

    def orderbook(self, o):
        return

