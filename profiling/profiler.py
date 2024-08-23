import pandas as pd
import os
from profiling.clusters.volume_profile import VolumeProfile


class Profile:
    """
    Market Profile class builds the profile of Volume and Delta.
    It processes each trade and updates the volume profile accordingly.
    """

    def __init__(self, tick_size, value_area_pct):
        self.tick_size = tick_size
        self.value_area_pct = value_area_pct
        self.volume_profile = VolumeProfile(value_area_pct, tick_size)
        self._initialize_info()

    def _initialize_info(self):
        """
        Initialize or reset the profile information.
        """
        self.info = {
            "first_trade_ts": None,
            "last_trade_ts": 0,
            "profiling": {},
        }

    def process_trade(self, trade):
        try:
            if self.info["first_trade_ts"] is None:
                self.info["first_trade_ts"] = trade.timestamp
            self.info["last_trade_ts"] = trade.timestamp
            self.info['profiling'] = self.volume_profile.update(trade.price, trade.side, trade.size)
        except Exception as err:
            print(f"Error updating profile with trade data: {err}")

    def reset_info(self):
        """
        Reset the profile information to its initial state.
        """
        self._initialize_info()
        self.volume_profile.reset_info()
