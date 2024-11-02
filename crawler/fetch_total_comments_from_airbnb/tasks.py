# Import the necessary modules
import requests  # The requests module is used for making HTTP requests in Python
from celery import shared_task  # Import shared_task from the Celery library to define asynchronous tasks

# Import utility functions for constructing the request and processing the response
from crawler.utils.request_content import \
    comment_request_from_airbnb  # Function to generate the request configuration for fetching comments from Airbnb
from crawler.utils.fetch_data import \
    get_comments_count_from_airbnb  # Function to extract the total number of comments from the Airbnb API response


# Define an asynchronous task using the shared_task decorator provided by Celery
@shared_task()
def fetch_total_comments(str_id, offset):
    """
    Asynchronous task to fetch the total number of comments for a specific Airbnb listing.

    Args:
        str_id (str): The unique identifier (string ID) for the Airbnb listing.
        offset (int): The offset parameter used for pagination, indicating the starting point for comments.

    Returns:
        int: The total number of comments for the Airbnb listing as extracted from the API response.
    """

    # Generate the request configuration (URL, headers, and parameters) needed to make the API call.
    # This is done by calling the comment_request_from_airbnb function with the listing ID and offset as inputs.
    request_config = comment_request_from_airbnb(str_id, offset)

    # Make an HTTP GET request to the Airbnb API using the generated configuration.
    # The request is sent to the URL specified in request_config[0], with headers request_config[1],
    # and query parameters request_config[2].
    response = requests.get(url=request_config[0], headers=request_config[1], params=request_config[2])

    # Extract the total number of comments from the JSON response using the get_comments_count_from_airbnb function.
    total_number = get_comments_count_from_airbnb(response.json())

    # Return the total number of comments.
    return total_number
