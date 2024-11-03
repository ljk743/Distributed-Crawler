# URL for the broker that Celery will use to send and receive messages.
# 'pyamqp' indicates the use of the AMQP protocol (usually RabbitMQ).
# The format is: 'protocol://username:password@hostname:port/vhost'
broker_url = 'pyamqp://leak990:ljk123456@192.168.56.102:30001/crawler'

# Backend configuration for storing task results.
# 'rpc://' uses RabbitMQ's built-in RPC mechanism for result storage.
result_backend = 'rpc://'

# Serialization configuration for tasks.
# Specifies that task arguments and results should be serialized as JSON.
task_serializer = 'json'
result_serializer = 'json'

# Only accept content types that are JSON.
# This is a security measure to ensure that only JSON-encoded data is processed.
accept_content = ['json']

# Timezone settings.
# Sets the timezone for the Celery application. 'UTC' is the standard universal time.
timezone = 'UTC'

# Enables the use of UTC.
# This ensures that all time-related operations use UTC as the standard.
enable_utc = True

# Task routing configuration.
# Uncomment and adjust this section if you need to route specific tasks to specific queues.
# This is useful in larger applications where different types of tasks might need to be handled by different workers.
# task_routes = {
#     'your_project.fetch_total_comments_from_booking.*': {'queue': 'default'},
# }

# Task acknowledgment configuration.
# 'task_acks_late' ensures that tasks are acknowledged only after they have been fully processed.
# This is useful for ensuring that tasks are not lost if a worker crashes before completing a task.
task_acks_late = True

# 'task_reject_on_worker_lost' ensures that if a worker is lost while processing a task,
# the task will be re-queued and processed by another worker.
task_reject_on_worker_lost = True

# Explanation of using multi-threading vs. multi-processing in Celery:
# Multi-threading in Celery can cause issues (bugs) because Python's Global Interpreter Lock (GIL) limits the execution
# of multiple threads in a single process. This can lead to problems, especially in I/O-bound and CPU-bound tasks.
# Therefore, the worker pool is set to 'prefork', which uses multi-processing. This allows each worker process to run
# independently, bypassing the GIL and making better use of multiple CPU cores.

# Use multi-processing instead of multi-threading for worker pools.
worker_pool = 'prefork'

# Task prefetching configuration.
# 'worker_prefetch_multiplier' controls how many tasks each worker pre-fetches from the broker.
# A higher number can improve performance by keeping workers busy but can also lead to uneven task distribution.
# Adjust this number based on the nature of your tasks and load.
worker_prefetch_multiplier = 5

# Logging configuration for workers.
# 'worker_hijack_root_logger' is set to False to prevent Celery from hijacking the root logger.
# This allows you to maintain control over logging configuration, especially if you have custom logging settings.
worker_hijack_root_logger = False

# Format for worker log messages.
# This format includes the timestamp, log level, and process name for better readability and debugging.
worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'

# Format for task log messages.
# This format includes additional information specific to tasks, such as the task name and task ID.
worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s'

# Other possible optimization settings:
# Uncomment and adjust the following setting if you need to limit the memory usage of worker processes.
# 'worker_max_memory_per_child' sets the maximum memory (in MB) that a worker process can use before it is restarted.
# This is useful for preventing memory leaks from consuming too much system memory.
# worker_max_memory_per_child = 12000  # Maximum memory per worker (in MB), adjust as needed.
