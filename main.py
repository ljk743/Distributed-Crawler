import multiprocessing
import subprocess

from airbnb import airbnb_run
from booking import booking_run
from webapp.application import app


def startup_airbnb():
    """
    Starts the process of fetching comments for a list of Airbnb listings.

    Returns:
        list: A list of Airbnb listing IDs that were processed.
    """
    str_ids = [
        "U3RheUxpc3Rpbmc6ODc5NjUxNjE3NDc1NDE4Mjg2",  # Airbnb listing ID
        "U3RheUxpc3Rpbmc6MjAyNTgyMjM=",  # Another Airbnb listing ID
        # Additional IDs can be added here
    ]
    airbnb_run(str_ids, batch_size=2, timeout=5)  # Run the Airbnb comment fetching process
    return str_ids  # Return the list of processed Airbnb IDs


def startup_booking():
    """
    Starts the process of fetching comments for a list of hotels from Booking.com.

    Returns:
        list: A list of hotel request dictionaries that were processed.
    """
    hotel_requests = [
        {'hotel_id': 4972311, 'ufi': -2601889, 'hotel_country_code': "gb"},  # Hotel request details
        # {'hotel_id': 5744683, 'ufi': -2601889, 'hotel_country_code': "gb"}  # Another hotel request (commented out)
        # Additional hotel requests can be added here
    ]
    booking_run(hotel_requests, batch_size=10)  # Run the Booking.com comment fetching process
    return hotel_requests  # Return the list of processed hotel requests


def startup_lit(path, port):
    """
    Starts the LIT (Language Interpretability Tool) server with the specified model and port.

    Args:
        path (str): The file path to the model or data to be loaded into LIT.
        port (int): The port number on which the LIT server will run.

    Returns:
        None
    """
    # Command to start the LIT server with the specified model file and port
    command = ['python', 'lit-nlp/load_model.py', '--file_path', path, "--port", str(port)]

    # Execute the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the standard output and error streams from the command execution
    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)


def start_flask():
    """
    Starts the Flask web application.

    Returns:
        None
    """
    app.run()  # Run the Flask app


if __name__ == '__main__':
    flag = "booking"  # Set the flag to either "airbnb" or "booking" to determine which process to run
    processes = []  # List to hold the multiprocessing Process objects

    if flag == "airbnb":
        # If the flag is set to "airbnb", start fetching Airbnb comments
        airbnb_task_ids = startup_airbnb()
        # For each Airbnb listing, start a LIT server process
        for i, airbnb_task_id in enumerate(airbnb_task_ids):
            p_airbnb = multiprocessing.Process(
                target=startup_lit,
                args=(f'shared_data/airbnb/airbnb_{airbnb_task_id}.csv', 5432 + i)  # Assign unique ports
            )
            processes.append(p_airbnb)  # Add the process to the list
            p_airbnb.start()  # Start the process

    if flag == "booking":
        # If the flag is set to "booking", start fetching Booking.com comments
        booking_tasks_ids = startup_booking()
        # For each hotel, start a LIT server process
        for i, booking_task_id in enumerate(booking_tasks_ids):
            p_booking = multiprocessing.Process(
                target=startup_lit,
                args=(f'shared_data/booking/booking_{booking_tasks_ids[i]["hotel_id"]}.csv', 5432 + i)  # Unique ports
            )
            processes.append(p_booking)  # Add the process to the list
            p_booking.start()  # Start the process

    # Start the Flask web application in a separate process
    p_flask = multiprocessing.Process(target=start_flask())
    processes.append(p_flask)  # Add the Flask process to the list
    p_flask.start()  # Start the Flask process

    # Wait for all child processes to complete
    try:
        for p in processes:
            p.join()  # Wait for each process to finish
    except KeyboardInterrupt:
        # If a manual interrupt (Ctrl+C) is detected, terminate all running processes
        print("Manual interrupt received. Terminating processes.")
        for p in processes:
            p.terminate()  # Terminate each process
            p.join()  # Ensure the process has fully stopped
