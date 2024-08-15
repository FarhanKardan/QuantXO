import time
from profiling.types.volume_profile import VolumeProfile
from profiling.types.open_interest_profile import OpenInterestProfile
from profiling.types.transactions import Transaction


# Market Profile class builds the profile or Volume, Delta, OI, Liquidation
class Profile:
    def __init__(self, queue, exchange, symbol, tick_size, value_area_pct):
        self.queue = queue
        self.tick_size = tick_size

        # creating volume profile
        self.volume_profile = VolumeProfile(value_area_pct)
        # creating open_interest profile
        self.open_interest_profile = OpenInterestProfile(value_area_pct)
        # creating a liquidation profile
        self.liquidation_profile = VolumeProfile(value_area_pct)

        # create transaction_size to differentiate based on buy/sell aggregated trade's size
        self.transaction = Transaction(100)

        # store information about general profile data
        self.info = {
            "open_time": time.time_ns(),
            "_time": 0,
            "last_trade_ts": 0,
            "value_area_pct": value_area_pct,
            "total_volume": 0,
            "instrument": {
                "exchange": exchange,
                "symbol": symbol,
                "init__funding_rate": 0,
                "init__open_interest": 0,
                "funding_rate": 0,
                "open_interest": 0,
                "open_interest_delta": 0,
                "last_trade_price": 0,
                "last_price": 0,
                "open_price": 0,
                "mark_price": 0,
                "price_change": 0,
            },
            "profile": 0,
            "transaction": 0,
        }

        # the status of the profile
        self.status = "OPEN"

    def close(self):
        # set the profile status to CLOSE
        self.status = "CLOSE"

        # publish an update with latest profile changes
        self.__publish_profile_update()

    '''Processing each trade and build the VolumeProfile'''
    def update_trade(self, t):
        try:
            # update the open price
            if self.info["instrument"]["open_price"] == 0:
                self.info["instrument"]["open_price"] = t.price
            else:
                price_change = t.price / self.info["instrument"]["open_price"]
                if price_change == 0:
                    price_change = 1
                self.info["instrument"]["price_change"] = price_change

            # update the last trade timestamp
            self.info["last_trade_ts"] = t.timestamp
            self.info["instrument"]["last_trade_price"] = t.price
            # find which bin the price belongs to
            index = self.__round_to_bin(t.price)

            # # update the transaction
            transaction = self.transaction.update(t.side, t.size, t.timestamp)
            self.info['transaction'] = transaction

            # update the volume profile
            p = self.volume_profile.update(index, t.side, t.size)
            self.info['profile'] = p
            self.info["total_volume"] += t.size

            # publish an update with latest profile changes
            self.__publish_profile_update()
            print(self.info)
        except Exception as err:
            print(err)
            print('Could not build the volume profile from the update {}')

    def update_instrument(self, inst):
        try:
            # update profile instrument information
            self.__update_profile_instrument_info(inst.funding_rate, inst.open_interest, inst.last_price,
                                                  inst.mark_price)

            # find which bin the price belongs to
            index = self.__round_to_bin(inst.last_price)

            # update open_interest profile
            self.open_interest_profile.update(index, inst.open_interest)

            # publish an update with latest profile changes
            self.__publish_profile_update()
        except Exception as err:
            print(err)
            print('Could not build the open_interest profile from the update {}')

    def update_liquidation(self, liq):
        try:
            # find which bin the price belongs to
            index = self.__round_to_bin(liq.price)

            side = "Buy"

            # flipping the side, because a buy liq, is a sell force order and vice versa
            if liq.side == "Buy":
                side = "Sell"
            elif liq.side == "Sell":
                side = "Buy"

            # update the liquidation profile
            self.liquidation_profile.update(index, side, liq.size)

            # publish an update with latest profile changes
            self.__publish_profile_update()
        except Exception as err:
            print(err)
            print('Could not build the liquidation profile from the update {}')

    def __update_profile_instrument_info(self, funding_rate, open_interest, last_price, mark_price):
        if self.info["instrument"]["init__funding_rate"] == 0:
            self.info["instrument"]["init__funding_rate"] = funding_rate

        if self.info["instrument"]["init__open_interest"] == 0:
            self.info["instrument"]["init__open_interest"] = open_interest

        self.info["instrument"]["funding_rate"] = funding_rate
        self.info["instrument"]["open_interest"] = open_interest
        self.info["instrument"]["mark_price"] = mark_price
        self.info["instrument"]["last_price"] = last_price

        self.info["instrument"]["open_interest_delta"] = \
            open_interest - self.info["instrument"]["init__open_interest"]

    '''Returning the index of a given tick based on the price and tick size'''
    def __round_to_bin(self, price):
        try:
            # Find the price idx of a new price from its reminding
            # price_idx = ((price // self.tick_size) * self.tick_size)
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
            # get the current timestamp
            timestamp = time.time_ns()

            # update the current time of profile
            self.info["_time"] = timestamp

            self.queue.put(self)
        except KeyError as err:
            print(err)
