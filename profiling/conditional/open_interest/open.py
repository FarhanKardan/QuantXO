from core.profile.conditional.base import BaseCondition


class OpenInterestOpen(BaseCondition):
    def __init__(self, exchange, symbol, tick_size, value_area_pct, total_open):
        super().__init__(exchange, symbol, tick_size, value_area_pct)

        self.total_open = total_open

    def trade(self, t):
        self.profile.update_trade(t)

    def instrument(self, i):
        total_open = self.profile.open_interest_profile.info['total_open']
        if total_open >= self.total_open:
            self.reset()

        self.profile.update_instrument(i)

    def liquidation(self, liq):
        self.profile.update_liquidation(liq)

    def orderbook(self, o):
        return

