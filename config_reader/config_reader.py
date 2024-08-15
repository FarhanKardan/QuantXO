import yaml


class ConfigReader:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Config file not found: {self.config_path}")
        except yaml.YAMLError as exc:
            raise Exception(f"Error parsing config file: {exc}")

    def get_binance_api_key(self):
        return self.config['binance']['api_key']

    def get_binance_api_secret(self):
        return self.config['binance']['api_secret']

    def get_influxdb_url(self):
        return self.config['influxdb']['url']

    def get_influxdb_token(self):
        return self.config['influxdb']['token']

    def get_influxdb_org(self):
        return self.config['influxdb']['org']

    def get_influxdb_bucket(self):
        return self.config['influxdb']['bucket']
