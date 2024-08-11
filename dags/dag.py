import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

# Add the parent directory to the system path to allow imports from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import pipeline functions from the pipelines module
from pipelines.aws_s3 import aws_s3_pipeline
from pipelines.reddit import reddit_pipeline


# Define default arguments for the DAG
default_args = {
    "owner": "Owner",
    "start_date": datetime(2024, 1, 17)  # DAG start date
}

# Get the current date in YYYYMMDD format to use as a suffix for file names
current_date_suffix = datetime.now().strftime("%Y%m%d")

# Define the DAG (Directed Acyclic Graph) for the Reddit ETL pipeline
dag = DAG(
    dag_id="reddit_etl_pipeline",  # Unique identifier for the DAG
    default_args=default_args,  # Default arguments to apply to all tasks
    schedule_interval="@daily",  # Schedule the DAG to run daily
    catchup=False,  # Do not catch up missed runs
    tags=["reddit", "etl", "data_pipeline"]  # Tags to categorize the DAG
)

# Task to extract data from Reddit
extract_data = PythonOperator(
    task_id="extract_reddit_data",  # Task identifier
    python_callable=reddit_pipeline,  # The function to call to execute the task
    op_kwargs={
        "file_name": f"reddit_{current_date_suffix}",  # File name with the current date suffix
        "subreddit": "dataengineering",  # Subreddit to extract data from
        "time_filter": "day",  # Time filter for Reddit posts (e.g., 'day', 'week')
        "limit": 500  # Limit the number of posts to extract
    },
    dag=dag,  # Associate the task with the DAG
)

# Task to upload the extracted data to S3
upload_to_s3 = PythonOperator(
    task_id="upload_to_s3",  # Task identifier
    python_callable=aws_s3_pipeline,  # The function to call to execute the task
    dag=dag,  # Associate the task with the DAG
)

# Define task dependencies (extract_data must run before upload_to_s3)
extract_data >> upload_to_s3
