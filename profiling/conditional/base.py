import uuid
from threading import Thread
from profiling.base import Profile
from queue import SimpleQueue
import pandas as pd


class BaseCondition:
    def __init__(self, tick_size, value_area_pct):
        self.id = uuid.uuid4()

        self.tick_size = tick_size
        self.value_area_pct = value_area_pct
        # self.feeder = ExchangeStream(exchange)

        self.threads = list()

        # setup the connections
        self.setup()

        self.send_queue = SimpleQueue()
        self.profile = Profile(self.send_queue, tick_size, value_area_pct)

    def subscribe(self):
        for profile in iter(self.send_queue.get, None):
            self.update(profile)
            yield profile

    # setup condition's prerequisites such as market data
    def setup(self):
        t = Thread(target=self.__process_trade)
        t.start()

    def disconnect(self):
        self.send_queue.put(None)
        # self.feeder.cancel_all()

        for t in self.threads:
            t.join()

        print('closed all threads')

    def get_queue(self):
        return self.send_queue

    def reset(self):
        self.profile.close()
        self.profile = Profile(self.send_queue, self.tick_size, self.value_area_pct)

    def update(self, p):
        return

    def trade(self, t):
        return

    def __process_trade(self):
        """
            Data Provider
        """
        try:
            df = pd.read_csv("/Users/farhan/Desktop/Data/BTCUSDT/BTCUSDT2024-08-09.csv.gz", compression="gzip")
            df = df[:1000]
            # responses = self.feeder.trade(self.symbol)
            for _, row in df.iterrows():
                self.trade(row)
            # for response in responses:
            #     self.trade(response)
        except Exception as err:
            self.send_queue.put(None)
