# Reddit Data ETL Pipeline

## Overview

This project sets up an ETL (Extract, Transform, Load) pipeline for extracting Reddit posts, transforming the data, and uploading it to AWS S3. It utilizes Apache Airflow for scheduling and orchestration, and Python scripts for data processing.

## Project Structure

- **`configs/config.conf`**: Configuration file containing database credentials, file paths, API keys, and AWS credentials.
- **`dags/dag.py`**: Apache Airflow DAG defining the workflow for extracting Reddit posts and uploading them to S3.
- **`etls/aws_s3.py`**: Script for managing interactions with AWS S3, including initializing connections, ensuring bucket existence, and uploading files.
- **`etls/reddit.py`**: Script for connecting to Reddit, fetching and transforming posts, and saving the data to a CSV file.
- **`pipelines/aws_s3.py`**: Script for executing the S3 upload pipeline, reading configuration, and performing the upload.
- **`pipelines/reddit.py`**: Script for executing the Reddit data extraction and transformation pipeline, reading configuration, and saving data to CSV.
- **`utils/constants.py`**: Utility file for storing configuration constants and settings.

## Configuration

1. **Database**: Settings for database connection such as host, name, port, user, and password.
2. **Paths**: Input and output directories for storing data files.
3. **API Keys**: Reddit API client ID and secret.
4. **AWS Credentials**: AWS credentials for accessing S3, including access key ID, secret access key, session token, region, and bucket name.
5. **ETL Settings**: Parameters for batch processing, error handling, and logging.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the Repository and Install Dependencies

```bash
git clone https://github.com/Ashwanth369/Reddit-Data-Engineering.git
cd Reddit-Data-Engineering
pip install -r requirements.txt
````

### 2. Configuration

Update the config/config.conf file with your credentials and settings:

- **Database Configuration**: Update the database connection details.
- **Reddit API**: Provide your Reddit API 'client_id' and 'secret_key'.
- **AWS S3**: Add your AWS credentials and S3 bucket details.

### 3. Build the Docker Image

Build the custom Docker image for Airflow using the provided Dockerfile:

```bash
docker-compose build
````

### 4. Initialize Airflow

Run the following command to initialize Airflow and set up the database:

```bash
docker-compose up airflow-init
````

### 5. Start the Airflow Services

Start the Airflow webserver, scheduler, and worker services:

```bash
docker-compose up -d
````

### 6. Access the Airflow UI

The Airflow web interface will be accessible at http://localhost:8080. Use the following credentials to log in:

- **Username**: admin
- **Password**: admin

### 7. Monitor and Trigger the DAG

- Navigate to the Airflow UI.
- Locate the reddit_etl_pipeline DAG.
- Trigger the DAG manually or wait for it to run on its daily schedule.
  
### 8. Cleanup

To stop the containers and clean up the environment, run:

```bash
docker-compose down --volumes
```

## ETL Workflow

1. **Extraction**:
   - Connect to Reddit using credentials from `configs/config.conf`.
   - Fetch posts from the specified subreddit and time filter.
   - Save the data to a CSV file.

2. **Transformation**:
   - Convert timestamps to datetime.
   - Transform and clean data fields as required.

3. **Loading**:
   - Upload the transformed CSV file to AWS S3.

## Notes

- Ensure that all necessary environment variables and configurations are set before running the pipeline.
- Customize the Reddit extraction parameters (e.g., subreddit, post limit) and S3 settings (e.g., bucket name) in the `configs/config.conf` file as needed.
- The pipeline is designed to run daily and will extract the top posts from the specified subreddit, process the data, and upload it to the configured S3 bucket.
- Logs and data outputs are stored in the logs/ and data/ directories, respectively.
