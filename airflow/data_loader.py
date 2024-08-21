from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests

# Define a function to download the file
def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded to {save_path}")

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 21),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'download_file_dag',
    default_args=default_args,
    description='A simple DAG to download a file',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Define the task using PythonOperator
    download_task = PythonOperator(
        task_id='download_file',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://example.com/file.zip',
            'save_path': '/path/to/save/file.zip',
        },
    )

    # Specify the task order (in this simple case, just the download task)
    download_task

