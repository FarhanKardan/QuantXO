import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
from config_reader.config_reader import ConfigReader


class InfluxDBWriter:
    def __init__(self, config_path='config.yaml'):
        self.config_reader = ConfigReader(config_path)
        url = self.config_reader.get_influxdb_url()
        token = self.config_reader.get_influxdb_token()
        org = self.config_reader.get_influxdb_org()
        bucket = self.config_reader.get_influxdb_bucket()

        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket = bucket
        self.org = org
        self.write_api = self.client.write_api(write_options=WriteOptions(batch_size=1000))

    def check_connection(self) -> bool:
        try:
            buckets_api = self.client.buckets_api()
            buckets = buckets_api.find_buckets()
            return bool(buckets)
        except Exception as e:
            print(f"Failed to connect to InfluxDB: {e}")
            return False

    def write_data(self, data: pd.DataFrame, measurement: str):
        points = []
        for _, row in data.iterrows():
            point = Point(measurement)
            for field in data.columns:
                point = point.field(field, row[field])
            point = point.time(row.name)
            points.append(point)

        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=points)
            print("Data written to InfluxDB successfully.")
        except Exception as e:
            print(f"Error writing data to InfluxDB: {e}")

    def query_data(self, flux_query: str) -> pd.DataFrame:
        try:
            query_api = self.client.query_api()
            tables = query_api.query(flux_query, org=self.org)
            results = []

            for table in tables:
                for record in table.records:
                    results.append(record.values)

            if results:
                df = pd.DataFrame(results)
                return df
            else:
                print("No data found for the query.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error querying data from InfluxDB: {e}")
            return pd.DataFrame()

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing InfluxDB client: {e}")
