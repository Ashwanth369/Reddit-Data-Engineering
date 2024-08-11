from etls.aws_s3 import connect_to_s3, create_bucket_if_not_exist, upload_to_s3
from utils.constants import AWS_BUCKET_NAME


def aws_s3_pipeline(ti):
    """
    Pipeline to upload a file to an AWS S3 bucket.
    
    Parameters:
        ti: An object from which to pull the file path using XCom in an Airflow task.
    """
    # Retrieve the file path from a previous Airflow task using XCom
    file_path = ti.xcom_pull(task_ids="extract_reddit_data", key="return_value")

    # Establish a connection to S3
    s3 = connect_to_s3()

    # Create the S3 bucket if it does not already exist
    create_bucket_if_not_exist(s3, AWS_BUCKET_NAME)

    # Upload the file to the S3 bucket
    upload_to_s3(s3, file_path, AWS_BUCKET_NAME, file_path.split("/")[-1])
