import threading
import time


class Transaction:
    def __init__(self, aggregate_rate=1):
        self.aggregate_rate = aggregate_rate

        self.transaction_size = {
            '20k':  {"bid": 0, "ask": 0, "delta": 0},
            '50k':  {"bid": 0, "ask": 0, "delta": 0},
            '100k': {"bid": 0, "ask": 0, "delta": 0},
            '200k': {"bid": 0, "ask": 0, "delta": 0},
            '400k': {"bid": 0, "ask": 0, "delta": 0},
            '1m':   {"bid": 0, "ask": 0, "delta": 0},
            '1m+':  {"bid": 0, "ask": 0, "delta": 0},
        }

        self.aggregate_sizes = {
            "buy": {
                "size": 0,
                "ts": None
            },
            "sell": {
                "size": 0,
                "ts": None
            }
        }

        self.__aggr_thread_timout = 0
        self.__aggr_thread_trigger = 500
        self.__aggr_thread = None
        self.__aggr_thread_stop_trigger = False

    def update(self, side, size, timestamp):
        side = side.lower()

        # if self.__aggr_thread is not None:
        #     # print('resetting aggr thread timeout')
        #     self.__aggr_thread_timout = 0

        # perform aggregation
        if self.aggregate_sizes[side]["ts"] is None:
            self.aggregate_sizes[side]["ts"] = timestamp
            self.aggregate_sizes[side]["size"] = size
        elif timestamp == self.aggregate_sizes[side]["ts"]:
            self.aggregate_sizes[side]["size"] += size
        elif timestamp > self.aggregate_sizes[side]["ts"]:
            # print("write aggregated trade, side: {}; aggr_size: {}".format(side, self.aggregate_sizes[side]["size"]))
            self.__update_transaction_sizes(side, self.aggregate_sizes[side]["size"])
            self.__clear_last_agg_trade(side)

        # if self.__aggr_thread is None:
        #     self.__aggr_thread = threading.Thread(target=self.__aggr_timeout,
        #                                           args=(lambda: self.__aggr_thread_stop_trigger, ))
        #     self.__aggr_thread.start()

    def __clear_last_agg_trade(self, side):
        self.aggregate_sizes[side]["size"] = 0
        self.aggregate_sizes[side]["ts"] = None

    def __update_transaction_sizes(self, side, size):
        """
        settle transaction sizes
        """
        category = Transaction.__get_transaction_size_category(size)
        if side == "buy":
            self.transaction_size[category]["bid"] += size
            self.transaction_size[category]["delta"] += size
        elif side == "sell":
            self.transaction_size[category]["ask"] += size
            self.transaction_size[category]["delta"] -= size

    @staticmethod
    def __get_transaction_size_category(size):
        if size < 20000:
            return '20k'
        elif 20000 <= size < 50000:
            return '50k'
        elif 50000 <= size < 100000:
            return '100k'
        elif 100000 <= size < 200000:
            return '200k'
        elif 200000 <= size < 400000:
            return '400k'
        elif 400000 <= size < 1000000:
            return '1m'
        elif size >= 1000000:
            return '1m+'

    def __aggr_timeout(self, stop):
        while True:
            if stop():
                print('stopped')
                break
            elif self.__aggr_thread_timout > self.__aggr_thread_trigger:
                # print('timeout triggered')
                self.__aggr_thread_timout = 0
                self.__update_transaction_sizes("buy", self.aggregate_sizes["buy"]["size"])
                self.__update_transaction_sizes("sell", self.aggregate_sizes["sell"]["size"])

                self.__clear_last_agg_trade("buy")
                self.__clear_last_agg_trade("sell")

                continue

            time.sleep(0.002)
            self.__aggr_thread_timout += 1
