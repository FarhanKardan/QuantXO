import requests
from datetime import datetime, timedelta
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


class BybitTickFetcher:
    def __init__(self, logger, base_uri="https://public.bybit.com/trading/BTCUSDT",
                 base_directory="/Users/farhan/Desktop/Data/BTCUSDT/", max_workers=10):
        self.logger = logger
        self.base_uri = base_uri
        self.base_directory = base_directory
        self.max_workers = max_workers
        os.makedirs(self.base_directory, exist_ok=True)

    def get_requests(self, path):
        url = f"{self.base_uri}/{path}"
        try:
            print("download start for", url)
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def file_writer(self, path, response):
        write_path = os.path.join(self.base_directory, path)
        try:
            with open(write_path, 'wb') as file:
                file.write(response.content)
            self.logger.info(f"Download completed for {path}")
        except IOError as e:
            self.logger.error(f"Error writing file {write_path}: {e}")

    def fetch_and_write(self, date):
        file_name = f"BTCUSDT{date.strftime('%Y-%m-%d')}.csv.gz"
        response = self.get_requests(file_name)
        if response:
            self.file_writer(file_name, response)

    def run(self, start_date, end_date):
        dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        for date in dates:
            self.fetch_and_write(date)


# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    fetcher = BybitTickFetcher(logger)
    start_date = datetime(2023, 1, 23)
    end_date = datetime(2023, 1, 30)
    fetcher.run(start_date, end_date)
