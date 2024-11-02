# Import the necessary modules
import requests  # The requests module is used for making HTTP requests in Python
from celery import shared_task  # Import shared_task from the Celery library to define asynchronous tasks

# Import utility functions for constructing the request and processing the response
from crawler.utils.request_content import \
    comments_request_form_booking  # Function to generate the request configuration for fetching comments from Booking.com
from crawler.utils.fetch_data import \
    get_comment_count_from_booking  # Function to extract the total number of comments from the Booking.com API response


# Define an asynchronous task using the shared_task decorator provided by Celery
@shared_task
def fetch_total_comments(skip, hotel_id, ufi, hotel_country_code):
    """
    Asynchronous task to fetch the total number of comments for a specific hotel on Booking.com.

    Args:
        skip (int): The number of comments to skip for pagination purposes.
        hotel_id (str): The unique identifier for the hotel on Booking.com.
        ufi (int): The unique identifier for the city or location where the hotel is situated.
        hotel_country_code (str): The country code where the hotel is located.

    Returns:
        int: The total number of comments for the hotel as extracted from the API response.
    """

    # Generate the request configuration (URL, headers, and JSON body) needed to make the API call.
    # This is done by calling the comments_request_form_booking function with the necessary inputs.
    request_config = comments_request_form_booking(hotel_id, ufi, hotel_country_code, skip)

    # Make an HTTP POST request to the Booking.com API using the generated configuration.
    # The request is sent to the URL specified in request_config[0], with headers request_config[1],
    # and the request body (JSON format) is specified in request_config[2].
    response = requests.post(url=request_config[0], headers=request_config[1], json=request_config[2])

    # Extract the total number of comments from the JSON response using the get_comment_count_from_booking function.
    count = get_comment_count_from_booking(response.json())

    # Return the total number of comments.
    return count
