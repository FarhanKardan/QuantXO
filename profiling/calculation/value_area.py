"""
    Calculating the value area
"""

import numpy as np


class ValueArea:
    @staticmethod
    def calculate_value_area(profile, value_area_pct, total_volume, poc_volume, poc_idx):
        target_vol = total_volume * value_area_pct
        trial_vol = poc_volume

        min_idx = poc_idx
        max_idx = poc_idx

        while trial_vol <= target_vol:
            last_min = min_idx
            last_max = max_idx

            next_min_idx = np.clip([min_idx - 1], 0, len(profile) - 1)
            next_max_idx = np.clip([max_idx + 1], 0, len(profile) - 1)

            low_volume = profile.iloc[next_min_idx] if next_min_idx != last_min else None
            high_volume = profile.iloc[next_max_idx] if next_max_idx != last_max else None

            if not high_volume or (low_volume and low_volume > high_volume):
                trial_vol += low_volume
                min_idx = next_min_idx
            elif not low_volume or (high_volume and low_volume <= high_volume):
                trial_vol += high_volume
                max_idx = next_max_idx
            else:
                break

        return profile.index[min_idx], profile.index[max_idx]

    """ Calculating the edges index for a given profile object """

    @staticmethod
    def get_edges(profile, value_area_pct, total_volume, poc_volume, poc_idx):
        if profile.size == 0:
            print('zero size')
        upper_edge_idx, lower_edge_idx = poc_idx, poc_idx
        target_vol = total_volume * value_area_pct
        area_volume, pointer = 0, 1
        if profile.size == 1:
            return profile.index[lower_edge_idx], profile.index[upper_edge_idx]
        else:
            area_volume = poc_volume
            while area_volume < target_vol:
                if 0 < lower_edge_idx and upper_edge_idx < profile.size:
                    upper_edge_idx += pointer
                    lower_edge_idx -= pointer
                elif lower_edge_idx == 0 and upper_edge_idx < profile.size:
                    upper_edge_idx += pointer
                elif upper_edge_idx == profile.size and lower_edge_idx > 0:
                    lower_edge_idx -= pointer
                area_volume = sum(profile.iloc[lower_edge_idx: upper_edge_idx])

            if upper_edge_idx == profile.size:
                return profile.index[lower_edge_idx], profile.index[upper_edge_idx - 1]

            return profile.index[lower_edge_idx], profile.index[upper_edge_idx]

