from binance.client import Client
from config_reader.config_reader import ConfigReader


class BinanceDataFetcher:
    def __init__(self, config_path='config.yaml'):
        self.config_reader = ConfigReader(config_path)
        api_key = self.config_reader.get_binance_api_key()
        api_secret = self.config_reader.get_binance_api_secret()
        self.client = Client(api_key, api_secret, tld="us")

    def check_binance_connection(self):
        try:
            self.client.ping()
            return True
        except Exception as e:
            print(f"Failed to connect to Binance API: {e}")
            return False

    def get_data(self, symbol, interval, start, end):
        from_d, from_m, from_y = start
        to_d, to_m, to_y = end
        range_from = f"{from_y}-{from_m:02d}-{from_d:02d}T00:00:00Z"
        range_to = f"{to_y}-{to_m:02d}-{to_d:02d}T00:00:00Z"

        try:
            klines = self.client.get_historical_klines(symbol, interval, range_from, range_to)
            return klines
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
