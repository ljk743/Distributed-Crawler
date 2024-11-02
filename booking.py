import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from celery import group

from crawler.fetch_comments_from_booking.tasks import fetch_comments
from crawler.fetch_total_comments_from_booking.tasks import fetch_total_comments
from utils.data_processing import booking_csv


def booking_comments(hotel_id, ufi, hotel_country_code, batch_size):
    """
    Fetch comments for a specific hotel from Booking.com and save them to JSON and CSV files.

    Args:
        hotel_id (str): The unique identifier for the hotel on Booking.com.
        ufi (str): A location-based identifier for the hotel (usually related to the city or region).
        hotel_country_code (str): The country code where the hotel is located.
        batch_size (int): The number of tasks to execute concurrently in a single batch.

    Returns:
        None
    """
    start_time = time.time()  # Record the start time for performance tracking
    json_output_path = f'shared_data/booking/booking_{hotel_id}.json'  # Path to save the JSON file
    csv_output_path = f'shared_data/booking/booking_{hotel_id}.csv'  # Path to save the CSV file

    # Fetch the total number of comments for the given hotel
    print(f"Fetching number of comments for hotel_id {hotel_id}...")
    count = fetch_total_comments(skip=0, hotel_id=hotel_id, ufi=ufi, hotel_country_code=hotel_country_code)
    print(f"Comments for hotel_id {hotel_id}: {count}")

    # Calculate the total number of tasks needed to fetch all comments
    print(f"Calculating number of fetch_total_comments_from_booking for hotel_id {hotel_id}...")
    comments_per_task = 10  # Each task will fetch 10 comments
    total_tasks = math.ceil(count / comments_per_task)  # Round up to ensure all comments are fetched
    print(f"Total fetch_total_comments_from_booking to be created for hotel_id {hotel_id}: {total_tasks}")

    print(f"Creating fetch_total_comments_from_booking for hotel_id {hotel_id}...")
    # Create a list of tasks to be executed by Celery
    tasks = []
    for i in range(total_tasks):
        skip = i * comments_per_task  # Calculate the skip value for each task
        tasks.append(fetch_comments.s(skip=skip, hotel_id=hotel_id, ufi=ufi, hotel_country_code=hotel_country_code))
    print(f"All fetch_total_comments_from_booking have been created for hotel_id {hotel_id}.")

    all_comments = []  # Initialize a list to store all fetched comments

    print(f"Executing fetch_total_comments_from_booking in batches for hotel_id {hotel_id}...")
    # Execute tasks in batches to control the load and manage execution
    for i in range(0, len(tasks), batch_size):
        batch_tasks = tasks[i:i + batch_size]  # Slice the tasks list to get the current batch
        task_group = group(batch_tasks)  # Create a Celery group for the current batch
        result = task_group.apply_async()  # Execute the batch asynchronously

        # Wait for the current batch of tasks to complete and retrieve results
        batch_results = result.get()

        # Process the results from the current batch and append them to the all_comments list
        for task_result in batch_results:
            all_comments.extend(task_result)

        # Pause for 3 seconds between batches to avoid overloading the server
        time.sleep(3)

    # Save the fetched comments to a JSON file
    with open(json_output_path, 'w', encoding='utf-8') as file:
        json.dump(all_comments, file, ensure_ascii=False, indent=4)
    print(f"Comments saved to {json_output_path}")

    # Convert the JSON file to CSV format
    booking_csv(json_output_path, csv_output_path)

    # Record the end time and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Crawler Time Usage: {elapsed_time} seconds")


def parallel_booking_comments(hotel_requests, batch_size):
    """
    Run the booking_comments function in parallel for multiple hotels using a process pool.

    Args:
        hotel_requests (list): A list of dictionaries containing hotel details (hotel_id, ufi, hotel_country_code).
        batch_size (int): The number of tasks to execute concurrently in a single batch.

    Returns:
        None
    """
    num_tasks = len(hotel_requests)  # Number of hotels to process
    max_workers = min(num_tasks, int(os.cpu_count() / 2))  # Dynamically adjust max_workers based on CPU count

    # Use ProcessPoolExecutor to execute booking_comments in parallel for each hotel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []  # List to hold future objects
        for req in hotel_requests:
            # Submit the booking_comments task for each hotel and store the future object
            futures.append(
                executor.submit(booking_comments, req['hotel_id'], req['ufi'], req['hotel_country_code'], batch_size))

        # Use as_completed to process tasks as they complete
        for future in as_completed(futures):
            try:
                result = future.result()  # Retrieve the result of the completed task or raise an exception
            except Exception as exc:
                print(f"Generated an exception: {exc}")  # Handle any exceptions that occurred during execution
            else:
                print(f"Task completed with result: {result}")  # Print the result if the task completed successfully


def booking_run(hotel_requests, batch_size):
    """
    Orchestrate the process of fetching comments and running LDA analysis for multiple hotels.

    Args:
        hotel_requests (list): A list of dictionaries containing hotel details (hotel_id, ufi, hotel_country_code).
        batch_size (int): The number of tasks to execute concurrently in a single batch.

    Returns:
        None
    """
    # Run the parallel fetching of comments
    parallel_booking_comments(hotel_requests, batch_size)

    # After fetching comments, run LDA analysis on the results for each hotel
    for hotel_request in hotel_requests:
        print(f'shared_data/booking/booking_{hotel_request["hotel_id"]}.csv')
        lda(f'shared_data/booking/booking_{hotel_request["hotel_id"]}.csv', categories=categories,
            threshold=1, topic_numbers_max=10)
