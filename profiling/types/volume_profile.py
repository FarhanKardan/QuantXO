import pandas as pd
from profiling.calculation.poc import POC
from profiling.calculation.value_area import ValueArea


class VolumeProfile:
    def __init__(self, value_area_pct):
        self.profile = {}
        self.value_area_pct = value_area_pct
        self.volume_cache = pd.Series(dtype=object)

        self.info = {
            "delta": 0,
            "trade_count": 0,
            "buy_trade_count": 0,
            "sell_trade_count": 0,
            "val": 0,
            "vah": 0,
            "poc": 0,
            "poc_idx": 0,
            "poc_volume": 0,
            "total_volume": 0,
            "bid_volume": 0,
            "ask_volume": 0
        }

    def update(self, index, side, size):
        try:
            self._update_profile(index, side, size)
            self._increment_trade_counts(side, size)

            self._calculate_poc()
            self._calculate_value_area()

            return self.profile
        except Exception as err:
            print(f"Error updating profile for tick {index}: {err}")

    def _update_profile(self, index, side, size):
        if index not in self.profile:
            self.profile[index] = self._create_new_profile(side, size)
        else:
            self._update_existing_profile(index, side, size)

        self._update_volume_cache(index, size)
        self._update_delta(side, size)

    def _create_new_profile(self, side, size):
        return {
            'volume': size,
            'bid': size if side == 'Buy' else 0,
            'ask': size if side == 'Sell' else 0,
            'delta': size if side == 'Buy' else -size,
            "t_count": 1,
            "t_b_count": 1 if side == 'Buy' else 0,
            "t_a_count": 1 if side == 'Sell' else 0
        }

    def _update_existing_profile(self, index, side, size):
        profile = self.profile[index]
        profile['volume'] += size
        profile['t_count'] += 1

        if side == 'Buy':
            profile['bid'] += size
            profile['delta'] += size
            profile['t_b_count'] += 1
            self.info['bid_volume'] += size
        elif side == 'Sell':
            profile['ask'] += size
            profile['delta'] -= size
            profile['t_a_count'] += 1
            self.info['ask_volume'] += size

    def _update_volume_cache(self, index, size):
        self.volume_cache[index] = self.volume_cache.get(index, 0) + size
        self.volume_cache.sort_index(inplace=True)

    def _increment_trade_counts(self, side, size):
        self.info['trade_count'] += 1
        if side == 'Buy':
            self.info['buy_trade_count'] += 1
        elif side == 'Sell':
            self.info['sell_trade_count'] += 1

        self.info['total_volume'] += size

    def _update_delta(self, side, size):
        self.info['delta'] += size if side == 'Buy' else -size

    def _calculate_poc(self):
        poc, poc_volume, poc_idx = POC.get_idx(self.volume_cache)
        self.info.update({"poc": poc, "poc_volume": poc_volume, "poc_idx": poc_idx})

    def _calculate_value_area(self):
        val, vah = ValueArea.get_edges(self.volume_cache, self.value_area_pct,
                                       self.info['total_volume'], self.info['poc_volume'],
                                       self.info['poc_idx'])
        self.info.update({"val": val, "vah": vah})
