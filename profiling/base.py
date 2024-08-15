import time
from profiling.types.volume_profile import VolumeProfile


# Market Profile class builds the profile of Volume and Delta
class Profile:
    def __init__(self, queue, tick_size, value_area_pct):
        self.queue = queue
        self.tick_size = tick_size

        # Creating volume profile
        self.volume_profile = VolumeProfile(value_area_pct)

        # Store information about general profile data
        self.info = {
            "open_time": time.time_ns(),
            "_time": 0,
            "last_trade_ts": 0,
            "value_area_pct": value_area_pct,
            "total_volume": 0,
            "profile": 0,
            "transaction": 0,
        }

        # The status of the profile
        self.status = "OPEN"

    def close(self):
        # Set the profile status to CLOSE
        self.status = "CLOSE"

        # Publish an update with latest profile changes
        self.__publish_profile_update()

    '''Processing each trade and build the VolumeProfile'''
    def update_trade(self, t):
        try:
            # Update the last trade timestamp
            self.info["last_trade_ts"] = t.timestamp

            # Find which bin the price belongs to
            index = self.__round_to_bin(t.price)

            # Update the volume profile
            p = self.volume_profile.update(index, t.side, t.size)
            self.info['profile'] = p
            self.info["total_volume"] += t.size


            # Publish an update with latest profile changes
            self.__publish_profile_update()
            print(self.info)
        except Exception as err:
            print(err)
            print('Could not build the volume profile from the update {}')

    '''Returning the index of a given tick based on the price and tick size'''
    def __round_to_bin(self, price):
        try:
            # Find the price index of a new price from its remainder
            if price % (self.tick_size * .5) < self.tick_size * .25:
                price_idx = (price - (price % (self.tick_size * .5)))
                return price_idx
            else:
                price_idx = (price - (price % (self.tick_size * .5))) + (self.tick_size * .5)
                return price_idx

        except Exception as err:
            print(err)
            print('Could not get the index of this {}'.format(self.tick_size))

    def __publish_profile_update(self):
        try:
            # Get the current timestamp
            timestamp = time.time_ns()

            # Update the current time of profile
            self.info["_time"] = timestamp

            self.queue.put(self)
        except KeyError as err:
            print(err)
