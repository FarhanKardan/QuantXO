from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import os
import logging
import requests


# def fetch_data(**kwargs):
#     url = kwargs.get('url')
#     logger = kwargs.get('logger')
#     try:
#         logger.info("Download start for %s", url)
#         response = requests.get(url)
#         response.raise_for_status()  # Raise HTTPError for bad responses
#         return response.content
#     except requests.RequestException as e:
#         logger.error("Error fetching %s: %s", url, e)
#         return None
#
#
# def write_data(**kwargs):
#     path = kwargs.get('path')
#     data = kwargs.get('data')
#     base_directory = kwargs.get('base_directory')
#     logger = kwargs.get('logger')
#     write_path = os.path.join(base_directory, path)
#     try:
#         with open(write_path, 'wb') as file:
#             file.write(data)
#         logger.info("Download completed for %s", path)
#     except IOError as e:
#         logger.error("Error writing file %s: %s", write_path, e)


def generate_dates(start_date, end_date):
    print("Generate the range we want to fetch data from")
    return [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]


# def fetch_and_write(**kwargs):
#     date = kwargs.get('date')
#     base_uri = kwargs.get('base_uri')
#     base_directory = kwargs.get('base_directory')
#     logger = kwargs.get('logger')
#     file_name = f"BTCUSDT{date.strftime('%Y-%m-%d')}.csv.gz"
#     url = f"{base_uri}/{file_name}"
#
#     # Fetch data
#     data = fetch_data(url=url, logger=logger)
#
#     if data:
#         # Write data
#         write_data(path=file_name, data=data, base_directory=base_directory, logger=logger)
#
#
# def run_fetching(start_date, end_date, base_uri, base_directory, logger):
#     dates = generate_dates(start_date, end_date)
#     for date in dates:
#         fetch_and_write(date=date, base_uri=base_uri, base_directory=base_directory, logger=logger)


# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': "farhan.kardan78@gmail.com",
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
        'bybit_tick_fetcher',
        default_args=default_args,
        description='Fetch and store Bybit BTCUSDT tick data',
        schedule_interval="@daily",
        start_date=days_ago(1),
        catchup=False) as f:

    # Define the PythonOperator tasks
    generate_dates = PythonOperator(
        task_id='generate_dates',
        python_callable=generate_dates,
        op_kwargs={
            'start_date': datetime(2023, 8, 23),
            'end_date': datetime(2023, 8, 30),
        }
    )


