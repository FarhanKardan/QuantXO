import requests
from datetime import timedelta
import os


class BybitTickFetcher:
    def __init__(self, logger, base_uri="https://public.bybit.com/trading/BTCUSDT",
                 base_directory="/Users/farhan/Desktop/Data/BTCUSDT/"):

        self.logger = logger
        self.base_uri = base_uri
        self.base_directory = base_directory
        os.makedirs(self.base_directory, exist_ok=True)

    def get_requests(self, path):
        url = f"{self.base_uri}/{path}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def file_writer(self, path):
        response = self.get_requests(path)
        if response:
            write_path = os.path.join(self.base_directory, path)
            try:
                with open(write_path, 'wb') as file:
                    file.write(response.content)
                self.logger.info(f"Download completed for {path}")
            except IOError as e:
                self.logger.error(f"Error writing file {write_path}: {e}")

    def run(self, start_date, end_date):
        current_date = start_date
        while current_date <= end_date:
            file_name = f"BTCUSDT{current_date.strftime('%Y-%m-%d')}.csv.gz"
            self.file_writer(file_name)
            current_date += timedelta(days=1)
