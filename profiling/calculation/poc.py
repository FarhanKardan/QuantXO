"""
    Calculating poc data
"""

import numpy as np


class POC:
    # find the index of the maximum closest to middle
    @staticmethod
    def get_idx(profile):
        # get the values of profile
        array = profile.values

        if len(array) == 0:
            return 0, 0, 0

        # find candidate maxima
        maxima_idxs = np.argwhere(array == np.amax(array))[:, 0]
        if len(maxima_idxs) == 1:
            poc_idx = maxima_idxs[0]
            poc = profile.index[poc_idx]
            poc_v = profile.iloc[poc_idx]

            return poc, poc_v, poc_idx
        elif len(maxima_idxs) <= 1:
            return 0, 0, 0

        # Find the distances from the midpoint to find
        # the maxima with the least distance
        midpoint = len(array) / 2
        v_norm = np.vectorize(np.linalg.norm)
        maximum_idx = np.argmin(v_norm(maxima_idxs - midpoint))

        poc_idx = maxima_idxs[maximum_idx]
        poc = profile.index[poc_idx]
        poc_v = profile.iloc[poc_idx]

        return poc, poc_v, poc_idx
