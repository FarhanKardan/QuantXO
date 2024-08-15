import pandas as pd

from profiling.calculation.poc import POC
from profiling.calculation.value_area import ValueArea


class OpenInterestProfile:
    def __init__(self, value_area_pct):
        self.profile = {}

        self.value_area_pct = value_area_pct

        self.__o_profile_volume_cache = pd.Series(dtype=object)
        self.__c_profile_volume_cache = pd.Series(dtype=object)

        self.info = {
            "delta": 0,
            "last_open_interest": 0,
            "last_price_index": 0,
            "o_val": 0,
            "o_vah": 0,
            "o_poc": 0,
            "o_poc_idx": 0,
            "o_poc_volume": 0,
            "c_val": 0,
            "c_vah": 0,
            "c_poc": 0,
            "c_poc_idx": 0,
            "c_poc_volume": 0,
            "total_open": 0,
            "total_close": 0,
        }

    def update(self, index, open_interest):
        try:
            if self.info["last_open_interest"] == 0 or self.info["last_price_index"] == 0:
                self.info["last_open_interest"] = open_interest
                self.info["last_price_index"] = index
            else:
                if self.info["last_price_index"] == index:
                    oi = open_interest - self.info["last_open_interest"]

                    # store the last price and open_interest
                    self.info["last_price_index"] = index
                    self.info["last_open_interest"] = open_interest

                    # update the index with updated OI
                    self.__update_profile(index, oi)

                    # calculate the POC based on open and close position separately
                    self.__calc_poc()
                    # calculating value area for opened/closed interest and closed interest
                    self.__calc_value_area()
                else:
                    oi = open_interest - self.info["last_open_interest"]

                    # store the last price and open_interest
                    self.info["last_price_index"] = index
                    self.info["last_open_interest"] = open_interest

                    # update half of the OI in previous last index and the other half into the new index
                    self.__update_profile(self.info["last_price_index"], int(oi / 2))
                    self.__update_profile(index, int(oi / 2))

                    # calculate the POC based on open and close position separately
                    self.__calc_poc()
                    # calculating value area for opened/closed interest and closed interest
                    self.__calc_value_area()
            return self.profile
        except Exception as err:
            print(err)
            print('Could not build the profile for the tick {}')

    def check_index(self, index):
        if index in self.profile:
            return True
        else:
            return False

    ''' Updating the profile based on a new tick'''
    def __update_profile(self, index, oi):
        try:
            self.__update_delta(oi)
            if index in self.profile:
                # opened interest
                if oi > 0:
                    self.profile[index]['volume'] += oi
                    self.profile[index]['open'] += oi
                    self.profile[index]['delta'] += oi

                # closed interest
                elif oi < 0:
                    self.profile[index]['volume'] += abs(oi)
                    self.profile[index]['close'] += abs(oi)
                    self.profile[index]['delta'] += oi
            else:
                self.__new_profile(index, oi)

            if oi > 0:
                # updating cached opened interest
                if index in self.__o_profile_volume_cache:
                    oi_cached = self.__o_profile_volume_cache.loc[index]
                    self.__o_profile_volume_cache[index] = oi_cached + oi
                else:
                    self.__o_profile_volume_cache[index] = oi
                    self.__o_profile_volume_cache.sort_index(inplace=True)
            elif oi < 0:
                # updating cached closed interest
                if index in self.__c_profile_volume_cache:
                    oi_cached = self.__c_profile_volume_cache.loc[index]
                    self.__c_profile_volume_cache[index] = oi_cached + abs(oi)
                else:
                    self.__c_profile_volume_cache[index] = abs(oi)
                    self.__c_profile_volume_cache.sort_index(inplace=True)
        except Exception as err:
            print(err)
            print('Could not update the profile of the {} {} {} {}')

    ''' Appending a new trade into the volume profiling'''
    def __new_profile(self, index, oi):
        try:
            new_volume_profile = dict()

            if oi > 0:
                new_volume_profile = {'volume': oi, 'open': oi, 'close': 0, 'delta': oi}
            elif oi < 0:
                new_volume_profile = {'volume': oi, 'open': 0, 'close': abs(oi), 'delta': oi}

            if len(new_volume_profile) > 0:
                self.profile[index] = new_volume_profile
        except Exception as err:
            print(err)
            print('Could not build the profile of the {} {}'.format(index, oi))

    def __update_delta(self, oi):
        self.info["delta"] += oi
        if oi > 0:
            self.info["total_open"] += oi
        elif oi < 0:
            self.info["total_close"] += abs(oi)

    def __calc_poc(self):
        if self.__o_profile_volume_cache.size > 0:
            # calculating POC for opened interest
            o_poc, o_poc_volume, o_poc_idx = POC.get_idx(self.__o_profile_volume_cache)
            self.info["o_poc"] = o_poc
            self.info["o_poc_volume"] = o_poc_volume
            self.info["o_poc_idx"] = o_poc_idx

        if self.__c_profile_volume_cache.size > 0:
            # calculating POC for closed interest
            c_poc, c_poc_volume, c_poc_idx = POC.get_idx(self.__c_profile_volume_cache)
            self.info["c_poc"] = c_poc
            self.info["c_poc_volume"] = c_poc_volume
            self.info["c_poc_idx"] = c_poc_idx

    def __calc_value_area(self):
        if self.__o_profile_volume_cache.size > 0:
            o_val, o_vah = ValueArea.get_edges(self.__o_profile_volume_cache, self.value_area_pct,
                                               self.info["total_open"], self.info["o_poc_volume"],
                                               self.info["o_poc_idx"])

            self.info["o_val"] = o_val
            self.info["o_vah"] = o_vah
        if self.__c_profile_volume_cache.size > 0:
            c_val, c_vah = ValueArea.get_edges(self.__c_profile_volume_cache, self.value_area_pct,
                                               self.info["total_close"], self.info["c_poc_volume"],
                                               self.info["c_poc_idx"])

            self.info["c_val"] = c_val
            self.info["c_vah"] = c_vah


