import pandas as pd
from profiling.calculation.poc import POC
from profiling.calculation.value_area import ValueArea


class VolumeProfile:
    def __init__(self, value_area_pct, tick_size):
        self.profile = {}
        self.value_area_pct = value_area_pct
        self.volume_cache = pd.Series(dtype=object)
        self.tick_size = tick_size

        self.info = {
            "total_volume": 0,
            "delta": 0,
            "trade_count": 0,
            "buy_trade_count": 0,
            "sell_trade_count": 0,
            "val": 0,
            "vah": 0,
            "poc": 0,
            "poc_idx": 0,
            "poc_volume": 0,
            "bid_volume": 0,
            "ask_volume": 0,
            "profiles": {}
        }

    def update(self, price, side, size):
        """Update the volume profile with new trade data."""
        try:
            price_index = self.__round_to_bin(price)
            self._update_profile(price_index, side, size)
            self._increment_trade_counts(side, size)

            # Calculate POC (Point of Control) and Value Area
            self._calculate_poc()
            self._calculate_value_area()

            self.info['profiles'] = self.profile
            return self.info

        except Exception as err:
            print(f"Error updating profile for price index {price_index}: {err}")

    def _update_profile(self, price_index, side, size):
        """Update the profile for the given price index."""
        if price_index not in self.profile:
            self.profile[price_index] = self._create_new_profile(side, size)
        else:
            self._update_existing_profile(price_index, side, size)

        self._update_volume_cache(price_index, size)
        self._update_delta(side, size)

    def _create_new_profile(self, side, size):
        """Create a new profile entry for a price index."""
        return {
            'volume': size,
            'bid': size if side == 'Buy' else 0,
            'ask': size if side == 'Sell' else 0,
            'delta': size if side == 'Buy' else -size,
            "t_count": 1,
            "t_b_count": 1 if side == 'Buy' else 0,
            "t_a_count": 1 if side == 'Sell' else 0
        }

    def _update_existing_profile(self, price_index, side, size):
        """Update an existing profile entry with new trade data."""
        profile = self.profile[price_index]
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

    def _update_volume_cache(self, price_index, size):
        """Update the volume cache and ensure it remains sorted."""
        if price_index in self.volume_cache:
            self.volume_cache[price_index] += size
        else:
            self.volume_cache[price_index] = size
        self.volume_cache.sort_index(inplace=True)

    def _increment_trade_counts(self, side, size):
        """Increment the trade counts based on the side of the trade."""
        self.info['trade_count'] += 1
        if side == 'Buy':
            self.info['buy_trade_count'] += 1
        elif side == 'Sell':
            self.info['sell_trade_count'] += 1

        self.info['total_volume'] += size

    def _update_delta(self, side, size):
        """Update the delta (net difference between buy and sell volume)."""
        self.info['delta'] += size if side == 'Buy' else -size

    def _calculate_poc(self):
        """Calculate the Point of Control (POC)."""
        poc, poc_volume, poc_idx = POC.get_idx(self.volume_cache)
        self.info.update({"poc": poc, "poc_volume": poc_volume, "poc_idx": poc_idx})

    def _calculate_value_area(self):
        """Calculate the Value Area Low (VAL) and Value Area High (VAH)."""
        val, vah = ValueArea.get_edges(
            self.volume_cache,
            self.value_area_pct,
            self.info['total_volume'],
            self.info['poc_volume'],
            self.info['poc_idx']
        )
        self.info.update({"val": val, "vah": vah})

    def __round_to_bin(self, price):
        """Round the price to the nearest tick size bin."""
        try:
            remainder = price % (self.tick_size * 0.5)
            if remainder < self.tick_size * 0.25:
                return price - remainder
            else:
                return price - remainder + (self.tick_size * 0.5)
        except Exception as err:
            print(f"Error rounding price {price} to bin: {err}")

    def _initialize_info(self):
        """Initialize or reset the profiling information."""
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
            "ask_volume": 0,
            "profiles": {}
        }

    def reset_info(self):
        """Reset the profiling information and clear the profile and volume cache."""
        self.profile = {}
        self.volume_cache = pd.Series(dtype=object)
        self._initialize_info()
