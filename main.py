from airbnb import airbnb_run


def startup_airbnb():
    """
    Starts the process of fetching comments for a list of Airbnb listings.

    Returns:
        list: A list of Airbnb listing IDs that were processed.
    """
    str_ids = ["U3RheUxpc3Rpbmc6ODc5NjUxNjE3NDc1NDE4Mjg2",  # Airbnb listing ID
        # "U3RheUxpc3Rpbmc6MjAyNTgyMjM=",  # Another Airbnb listing ID
        # Additional IDs can be added here
    ]
    airbnb_run(str_ids, batch_size=2, timeout=5)  # Run the Airbnb comment fetching process
    return str_ids  # Return the list of processed Airbnb IDs



if __name__ == '__main__':
    airbnb_task_ids = startup_airbnb()

