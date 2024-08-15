from profiling.conditional.base import BaseCondition


class ProfileVolume(BaseCondition):

    def __init__(self, exchange, symbol, tick_size, value_area_pct, volume):
        super().__init__(exchange, symbol, tick_size, value_area_pct)

        self.volume = volume

    # profile update will receive here, don't implement logic here, as it lags from the realtime data,
    # because of underlying queue mechanism implemented
    def update(self, p):
        pass

    def trade(self, t):
        if self.profile.volume_profile.info['total_volume'] >= self.volume:
            self.reset()

        self.profile.update_trade(t)

    def instrument(self, i):
        self.profile.update_instrument(i)

    def liquidation(self, liq):
        self.profile.update_liquidation(liq)

    def orderbook(self, o):
        return
