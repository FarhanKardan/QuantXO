import numpy as np


class ValueArea:
    @staticmethod
    def calculate_value_area(profile, value_area_pct, total_volume, poc_volume, poc_idx):
        target_vol = total_volume * value_area_pct
        trial_vol = poc_volume

        min_idx = poc_idx
        max_idx = poc_idx

        profile_len = len(profile)

        while trial_vol < target_vol and (min_idx > 0 or max_idx < profile_len - 1):
            if min_idx > 0 and (max_idx == profile_len - 1 or profile.iloc[min_idx - 1] >= profile.iloc[max_idx + 1]):
                trial_vol += profile.iloc[min_idx - 1]
                min_idx -= 1
            elif max_idx < profile_len - 1:
                trial_vol += profile.iloc[max_idx + 1]
                max_idx += 1
            else:
                break

        return profile.index[min_idx], profile.index[max_idx]

    @staticmethod
    def get_edges(profile, value_area_pct, total_volume, poc_volume, poc_idx):
        if profile.size == 0:
            raise ValueError("Profile is empty")

        profile_len = len(profile)
        target_vol = total_volume * value_area_pct
        area_volume = poc_volume

        lower_edge_idx = poc_idx
        upper_edge_idx = poc_idx

        while area_volume < target_vol and (lower_edge_idx > 0 or upper_edge_idx < profile_len - 1):
            if lower_edge_idx > 0 and (
                    upper_edge_idx == profile_len - 1 or profile.iloc[lower_edge_idx - 1] >= profile.iloc[
                upper_edge_idx + 1]):
                area_volume += profile.iloc[lower_edge_idx - 1]
                lower_edge_idx -= 1
            elif upper_edge_idx < profile_len - 1:
                area_volume += profile.iloc[upper_edge_idx + 1]
                upper_edge_idx += 1
            else:
                break

        if upper_edge_idx == profile_len - 1:
            return profile.index[lower_edge_idx], profile.index[upper_edge_idx]

        return profile.index[lower_edge_idx], profile.index[upper_edge_idx]
