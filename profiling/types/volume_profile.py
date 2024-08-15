import pandas as pd
from profiling.calculation.poc import POC
from profiling.calculation.value_area import ValueArea


class VolumeProfile:
    def __init__(self, value_area_pct):
        self.profile = {}
        self.value_are_pct = value_area_pct
        self.__profile_volume_cache = pd.Series(dtype=object)

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
            self.__update_profile(index, side, size)
            self.__add_trade_count(side)

            # updating total volume
            self.info["total_volume"] += size

            # calculating POC for the volume profile
            self.__calc_poc()

            # calculating value area high/low for the volume profile
            self.__cal_value_area()

            return self.profile
        except Exception as err:
            print(err)
            print('Could not build the profile for the tick {}')

    ''' Updating the profile based on a new tick'''
    def __update_profile(self, index, side, size):
        try:
            self.__update_delta(side, size)
            if index in self.profile:
                self.profile[index]['volume'] += size
                if side == 'Buy':
                    self.profile[index]['bid'] += size
                    self.profile[index]['delta'] += size
                    self.profile[index]['t_count'] += 1
                    self.profile[index]['t_b_count'] += 1

                    # updating buy total volume
                    self.info["bid_volume"] += size

                elif side == 'Sell':
                    self.profile[index]['ask'] += size
                    self.profile[index]['delta'] -= size
                    self.profile[index]['t_count'] += 1
                    self.profile[index]['t_a_count'] += 1

                    # updating sell total volume
                    self.info["ask_volume"] += size
            else:
                self.__new_profile(index, side, size)

            # updating buy total volume
            if index in self.__profile_volume_cache:
                vol = self.__profile_volume_cache.loc[index]
                self.__profile_volume_cache[index] = vol + size
            else:
                self.__profile_volume_cache[index] = size
                self.__profile_volume_cache.sort_index(inplace=True)
        except Exception as err:
            print(err)
            print('Could not update the profile of the {} {} {} {}')

    ''' Appending a new trade into the volume profiling'''
    def __new_profile(self, index, side, size):
        try:
            new_volume_profile = dict()

            if side == 'Buy':
                new_volume_profile = {'volume': size, 'bid': size, 'ask': 0, 'delta': size,
                                      "t_count": 1, "t_b_count": 1, "t_a_count": 0}
            elif side == 'Sell':
                new_volume_profile = {'volume': size, 'bid': 0, 'ask': size, 'delta': -size,
                                      "t_count": 1, "t_b_count": 0, "t_a_count": 1}
            else:
                print('the side is not available')

            if len(new_volume_profile) > 0:
                self.profile[index] = new_volume_profile
        except Exception as err:
            print(err)
            print('Could not build the profile of the {} {} {}'.format(index, side, size))

    def __add_trade_count(self, side):
        if side == 'Buy':
            self.info["buy_trade_count"] += 1
        elif side == 'Sell':
            self.info["sell_trade_count"] += 1

        self.info["trade_count"] += 1

    def __update_delta(self, side, size):
        if side == "Buy":
            self.info["delta"] += size
        elif side == "Sell":
            self.info["delta"] -= size

    def __calc_poc(self):
        poc, poc_volume, poc_idx = POC.get_idx(self.__profile_volume_cache)
        self.info["poc"] = poc
        self.info["poc_volume"] = poc_volume
        self.info["poc_idx"] = poc_idx

    def __cal_value_area(self):
        val, vah = ValueArea.get_edges(self.__profile_volume_cache, self.value_are_pct, self.info["total_volume"],
                                       self.info["poc_volume"],  self.info["poc_idx"])

        self.info["val"] = val
        self.info["vah"] = vah
