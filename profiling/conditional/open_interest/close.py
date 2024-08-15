from core.profile.conditional.base import BaseCondition


class OpenInterestClose(BaseCondition):
    def __init__(self, exchange, symbol, tick_size, value_area_pct, total_close):
        super().__init__(exchange, symbol, tick_size, value_area_pct)

        self.total_close = total_close

    def trade(self, t):
        self.profile.update_trade(t)

    def instrument(self, i):
        total_close = self.profile.open_interest_profile.info['total_close']
        if total_close >= self.total_close:
            self.reset()

        self.profile.update_instrument(i)

    def liquidation(self, liq):
        self.profile.update_liquidation(liq)

    def orderbook(self, o):
        return

