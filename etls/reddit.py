import sys

import numpy as np
import pandas as pd
import praw
from praw import Reddit

from utils.constants import POST_FIELDS


def reddit_connection(client_id, client_secret, user_agent):
    """
    Establish a connection to the Reddit API using provided credentials.
    
    Parameters:
        client_id (str): Reddit API client ID.
        client_secret (str): Reddit API client secret.
        user_agent (str): User agent string to identify the application.
    
    Returns:
        Reddit: An instance of the Reddit API client.
    """
    try:
        # Initialize Reddit instance with credentials
        reddit_instance = praw.Reddit(client_id=client_id,
                                      client_secret=client_secret,
                                      user_agent=user_agent)
        print("Successfully connected to Reddit!")
        return reddit_instance
    except Exception as error:
        # Print error message and exit if connection fails
        print(f"Connection error: {error}")
        sys.exit(1)


def extract_data(reddit_instance: Reddit, subreddit_name: str, time_period: str, post_limit=None):
    """
    Extract top posts from a specified subreddit.
    
    Parameters:
        reddit_instance (Reddit): An instance of the Reddit API client.
        subreddit_name (str): The name of the subreddit to extract posts from.
        time_period (str): The time filter to apply (e.g., "day", "week", "month").
        post_limit (int): The maximum number of posts to extract. If None, all available posts are retrieved.
    
    Returns:
        list: A list of dictionaries containing the extracted post data.
    """
    # Access subreddit and retrieve top posts
    subreddit = reddit_instance.subreddit(subreddit_name)
    retrieved_posts = subreddit.top(time_filter=time_period, limit=post_limit)

    posts_data = []

    # Extract required fields from each post
    for post in retrieved_posts:
        post_details = vars(post)
        # Filter and keep only the required fields as specified in POST_FIELDS
        filtered_post = {field: post_details[field] for field in POST_FIELDS}
        posts_data.append(filtered_post)

    return posts_data


def transform_data(posts_dataframe: pd.DataFrame):
    """
    Transform the extracted data into a more usable format.
    
    Parameters:
        posts_dataframe (pd.DataFrame): DataFrame containing the extracted post data.
    
    Returns:
        pd.DataFrame: Transformed DataFrame with necessary adjustments.
    """
    # Convert Unix timestamp to datetime format
    posts_dataframe["created_utc"] = pd.to_datetime(posts_dataframe["created_utc"], unit="s")
    
    # Normalize "over_18" field to boolean values
    posts_dataframe["over_18"] = posts_dataframe["over_18"].apply(lambda x: True if x else False)
    
    # Ensure author field is of string type
    posts_dataframe["author"] = posts_dataframe["author"].astype(str)
    
    # Handle missing or unknown values in the "edited" field
    common_edited_value = posts_dataframe["edited"].mode()[0]
    posts_dataframe["edited"] = posts_dataframe["edited"].apply(
        lambda x: x if x in [True, False] else common_edited_value
    ).astype(bool)
    
    # Convert numeric fields to integers
    posts_dataframe["num_comments"] = posts_dataframe["num_comments"].astype(int)
    posts_dataframe["score"] = posts_dataframe["score"].astype(int)
    
    # Ensure title field is of string type
    posts_dataframe["title"] = posts_dataframe["title"].astype(str)

    return posts_dataframe


def load_data(data: pd.DataFrame, file_path: str):
    """
    Save the transformed data to a CSV file.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the transformed data.
        file_path (str): The file path where the CSV will be saved.
    """
    # Save the DataFrame to a CSV file without the index
    data.to_csv(file_path, index=False)
