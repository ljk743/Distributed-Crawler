import json
import math
import time
from concurrent.futures import ProcessPoolExecutor

from celery import group

from crawler.fetch_comments_from_airbnb.tasks import fetch_comments
from crawler.fetch_total_comments_from_airbnb.tasks import fetch_total_comments
from utils.data_processing import airbnb_csv


def airbnb_comments(str_id, batch_size, timeout):
    """
    Fetch comments for a specific Airbnb listing and save them to CSV and JSON files.

    Args:
        str_id (str): The Airbnb listing ID.
        batch_size (int): The number of tasks to execute concurrently in a single batch.
        timeout (int): The maximum time (in seconds) to wait for each batch of tasks to complete.

    Returns:
        None
    """
    start_time = time.time()  # Record the start time for performance tracking
    csv_output_path = f'shared_data/airbnb/airbnb_{str_id}.csv'  # Path to save the CSV file
    json_output_path = f'shared_data/airbnb/airbnb_{str_id}.json'  # Path to save the JSON file

    # Fetch the total number of comments for the given listing ID
    print(f"Fetching number of comments for {str_id}...")
    total_comments = fetch_total_comments(str_id, offset=0)
    print(f"Total comments for {str_id}: {total_comments}")

    # Calculate the total number of tasks needed to fetch all comments
    comments_per_task = 50  # Each task will fetch 50 comments
    total_tasks = math.ceil(total_comments / comments_per_task)  # Round up to ensure all comments are fetched
    print(f"Total tasks to be created for {str_id}: {total_tasks}")

    print(f"Creating tasks for {str_id}...")
    # Create a list of tasks to be executed by Celery
    tasks = []
    for i in range(total_tasks):
        offset = i * comments_per_task  # Calculate the offset for each task
        tasks.append(fetch_comments.s(str_id=str_id, offset=offset))  # Add the task to the list
    print(f"All tasks have been created for {str_id}.")

    all_comments = []  # Initialize a list to store all fetched comments

    print(f"Executing tasks in batches for {str_id}...")
    # Execute tasks in batches to control the load and manage execution
    for i in range(0, len(tasks), batch_size):
        batch_tasks = tasks[i:i + batch_size]  # Slice the tasks list to get the current batch
        task_group = group(batch_tasks)  # Create a Celery group for the current batch
        result = task_group.apply_async()  # Execute the batch asynchronously

        # Wait for the current batch of tasks to complete with a specified timeout
        batch_results = result.get(timeout=timeout)
        all_comments.extend(batch_results)  # Append the results to the list of all comments

        # Pause for 3 seconds between batches to avoid overloading the server
        time.sleep(3)

    # Save the results to a JSON file
    with open(json_output_path, 'w', encoding='utf-8') as file:
        json.dump(all_comments, file, ensure_ascii=False, indent=4)
    print(f"Comments have saved to {json_output_path}")

    # Convert the JSON file to CSV format
    airbnb_csv(json_output_path, csv_output_path)

    # Record the end time and calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Crawler Time Usage: {elapsed_time} seconds")


def parallel_airbnb_comments(ids, batch_size, timeout):
    """
    Run the airbnb_comments function in parallel for multiple listing IDs.

    Args:
        ids (list): A list of Airbnb listing IDs.
        batch_size (int): The number of tasks to execute concurrently in a single batch.
        timeout (int): The maximum time (in seconds) to wait for each batch of tasks to complete.

    Returns:
        None
    """
    # Use ProcessPoolExecutor to execute airbnb_comments in parallel for each ID
    with ProcessPoolExecutor(max_workers=len(ids)) as executor:
        # Submit tasks to the executor for each listing ID
        futures = [
            executor.submit(airbnb_comments, str_id, batch_size, timeout)
            for i, str_id in enumerate(ids)
        ]

        # Wait for all futures to complete
        for future in futures:
            future.result()  # This blocks until the individual task is completed


def airbnb_run(str_ids, batch_size, timeout):
    """
    Orchestrate the process of fetching comments and running LDA (Latent Dirichlet Allocation)
    analysis for multiple Airbnb listings.

    Args:
        str_ids (list): A list of Airbnb listing IDs.
        batch_size (int): The number of tasks to execute concurrently in a single batch.
        timeout (int): The maximum time (in seconds) to wait for each batch of tasks to complete.

    Returns:
        None
    """
    # Run the parallel fetching of comments
    parallel_airbnb_comments(str_ids, batch_size, timeout)
