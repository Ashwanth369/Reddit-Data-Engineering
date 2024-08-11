import pandas as pd

from etls.reddit import reddit_connection, extract_data, transform_data, load_data
from utils.constants import CLIENT_ID, SECRET, OUTPUT_PATH


def reddit_pipeline(file_name: str, subreddit: str, time_filter="day", limit=None):
    """
    Executes a data pipeline to extract, transform, and load Reddit posts from a specified subreddit.
    
    Parameters:
        file_name (str): The name of the output file (without extension).
        subreddit (str): The name of the subreddit to extract data from.
        time_filter (str): The time filter to apply (e.g., "day", "week", "month"). Default is "day".
        limit (int): The maximum number of posts to extract. If None, all available posts are extracted.
    
    Returns:
        str: The file path of the saved CSV file.
    """
    # Establish a connection to the Reddit API using provided credentials
    instance = reddit_connection(CLIENT_ID, SECRET, "Anonymous Bot")

    # Extract posts from the specified subreddit using the provided time filter and limit
    posts = extract_data(instance, subreddit, time_filter, limit)

    # Convert the extracted posts into a DataFrame
    post_df = pd.DataFrame(posts)
    
    # Transform the DataFrame as needed (e.g., cleaning, feature engineering)
    post_df = transform_data(post_df)

    # Define the output file path for the CSV file
    file_path = f"{OUTPUT_PATH}/{file_name}.csv"
    
    # Load the transformed data into the CSV file at the specified path
    load_data(post_df, file_path)

    # Return the file path of the saved CSV file
    return file_path
