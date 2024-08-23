import numpy as np


class POC:
    @staticmethod
    def get_idx(profile):
        # Convert profile to a NumPy array and index array
        array = profile.values
        index = profile.index

        if len(array) == 0:
            return 0, 0, 0

        # Find the index of the maximum value
        max_value = np.max(array)
        maxima_idxs = np.where(array == max_value)[0]

        if len(maxima_idxs) == 0:
            return 0, 0, 0

        # If only one maximum value, return its details
        if len(maxima_idxs) == 1:
            poc_idx = maxima_idxs[0]
            poc = index[poc_idx]
            poc_v = array[poc_idx]
            return poc, poc_v, poc_idx

        # Find the midpoint of the array
        midpoint = len(array) / 2

        # Compute distances from the midpoint
        distances = np.abs(maxima_idxs - midpoint)

        # Find the index of the minimum distance
        closest_maxima_idx = maxima_idxs[np.argmin(distances)]

        poc = index[closest_maxima_idx]
        poc_v = array[closest_maxima_idx]

        return poc, poc_v, closest_maxima_idx
