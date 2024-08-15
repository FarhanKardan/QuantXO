import time
from profiling.clusters.volume_profile import VolumeProfile


class Profile:
    """
    Market Profile class builds the profile of Volume and Delta.
    It processes each trade and updates the volume profile accordingly.
    """

    def __init__(self, queue, tick_size, value_area_pct):
        self.queue = queue
        self.tick_size = tick_size
        self.value_area_pct = value_area_pct

        # Create a VolumeProfile instance
        self.volume_profile = VolumeProfile(value_area_pct, tick_size)

        # Initialize profile information
        self.info = {
            "open_time": time.time_ns(),
            "_time": 0,
            "last_trade_ts": 0,
            "value_area_pct": value_area_pct,
            "profiling": {},
        }

        # Profile status
        self.status = "OPEN"

    def close(self):
        """
        Close the profile by setting the status to 'CLOSE'
        and publishing the final profile update.
        """
        self.status = "CLOSE"
        self.__publish_profile_update()

    def update_trade(self, trade):
        """
        Update the profile with new trade data.

        Args:
            trade: An object representing a trade with attributes 'price', 'side', 'size', and 'timestamp'.
        """
        try:
            # Update the timestamp of the last trade
            self.info["last_trade_ts"] = trade.timestamp

            # Update the volume profile and store the result in 'profiling'
            self.info['profiling'] = self.volume_profile.update(trade.price, trade.side, trade.size)

            # Publish the updated profile
            self.__publish_profile_update()

        except Exception as err:
            print(f"Error updating profile with trade data: {err}")

    def __publish_profile_update(self):
        """
        Publish the updated profile to the queue.
        """
        try:
            # Update the current timestamp
            self.info["_time"] = time.time_ns()

            # Put the updated profile in the queue
            self.queue.put(self)

        except KeyError as err:
            print(f"Error publishing profile update: {err}")
