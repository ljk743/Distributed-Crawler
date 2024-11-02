# Import the necessary modules
import requests  # The requests module is used for making HTTP requests in Python
from celery import shared_task  # Import shared_task from the Celery library to define asynchronous tasks

# Import the function that constructs the request configuration for fetching comments from Airbnb
from crawler.utils.request_content import comment_request_from_airbnb


# Define an asynchronous task using the shared_task decorator provided by Celery
@shared_task()
def fetch_comments(str_id, offset):
    """
    Asynchronous task to fetch comments for a specific Airbnb listing.

    Args:
        str_id (str): The unique identifier (string ID) for the Airbnb listing.
        offset (int): The offset parameter used for pagination, indicating the starting point for comments.

    Returns:
        dict: The JSON response from the Airbnb API, containing the fetched comments data.
    """

    # Generate the request configuration (URL, headers, and parameters) needed to make the API call.
    # This is done by calling the comment_request_from_airbnb function with the listing ID and offset as inputs.
    request_config = comment_request_from_airbnb(str_id, offset)

    # Make an HTTP GET request to the Airbnb API using the generated configuration.
    # The request is sent to the URL specified in request_config[0], with headers request_config[1],
    # and query parameters request_config[2].
    response = requests.get(url=request_config[0], headers=request_config[1], params=request_config[2])

    # Return the JSON content of the response. This typically contains the comments data in dictionary format.
    return response.json()
