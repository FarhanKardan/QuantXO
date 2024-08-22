# hello_world_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import timedelta

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval=timedelta(days=1),
)

# Define the Python function to run
def print_hello_world():
    print("Hello, world!")

# Define the task using PythonOperator
task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello_world,
    dag=dag,
)

# Set the task dependencies
task
