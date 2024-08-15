from core.profile.conditional.base import BaseCondition


class LiquidationVolume(BaseCondition):
    def __init__(self, exchange, symbol, tick_size, value_area_pct, volume):
        super().__init__(exchange, symbol, tick_size, value_area_pct)

        self.volume = volume

    def trade(self, t):
        self.profile.update_trade(t)

    def instrument(self, i):
        self.profile.update_instrument(i)

    def liquidation(self, liq):
        volume = self.profile.liquidation_profile.info['total_volume']
        if volume >= self.volume:
            self.reset()

        self.profile.update_liquidation(liq)

    def orderbook(self, o):
        return

