import s3fs
from utils.constants import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY


def connect_to_s3():
    """
    Establish a connection to AWS S3 using s3fs with provided access credentials.
    
    Returns:
        s3fs.S3FileSystem: A filesystem object representing the S3 connection.
    """
    try:
        # Create an S3 filesystem object using the provided AWS access key ID and secret key
        s3 = s3fs.S3FileSystem(anon=False,
                               key=AWS_ACCESS_KEY_ID,
                               secret=AWS_ACCESS_KEY)
        return s3
    except Exception as e:
        # Print the exception if the connection fails
        print(e)


def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket: str):
    """
    Create an S3 bucket if it does not already exist.
    
    Parameters:
        s3 (s3fs.S3FileSystem): The S3 filesystem object.
        bucket (str): The name of the S3 bucket to create or check.
    """
    try:
        # Check if the bucket already exists
        if not s3.exists(bucket):
            # Create the bucket if it does not exist
            s3.mkdir(bucket)
            print("Bucket created")
        else:
            # Inform the user if the bucket already exists
            print("Bucket already exists")
    except Exception as e:
        # Print the exception if bucket creation or existence check fails
        print(e)


def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket: str, s3_file_name: str):
    """
    Upload a file to a specified S3 bucket.
    
    Parameters:
        s3 (s3fs.S3FileSystem): The S3 filesystem object.
        file_path (str): The local file path of the file to upload.
        bucket (str): The name of the S3 bucket to upload the file to.
        s3_file_name (str): The name of the file in S3 after upload.
    """
    try:
        # Upload the file to the specified S3 bucket under the 'raw' directory
        s3.put(file_path, bucket + "/raw/" + s3_file_name)
        print("File uploaded to s3")
    except FileNotFoundError:
        # Print a message if the file to be uploaded is not found
        print("The file was not found")
