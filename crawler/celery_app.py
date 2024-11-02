# Import the Celery class from the celery module
from celery import Celery

# Create an instance of the Celery class with the name 'crawler'
# This name is typically the name of your project or a specific part of your application
app = Celery('crawler')

# Load the configuration settings for Celery from an external configuration file or module
# The configuration is being loaded from a module named 'crawler.celery_config'
app.config_from_object('crawler.celery_config')

# Automatically discover tasks from specified modules
# The modules listed are:
# - 'crawler.fetch_total_comments_from_booking': This module likely contains tasks related to fetching the total number of comments from Booking.com.
# - 'crawler.fetch_comments_from_booking': This module likely contains tasks related to fetching comments from Booking.com.
# - 'crawler.fetch_comments_from_airbnb': This module likely contains tasks related to fetching comments from Airbnb.
# Celery will search these modules for any task definitions (functions decorated with @shared_task or @task) and register them with the Celery application.
app.autodiscover_tasks(['crawler.fetch_total_comments_from_booking',
                        'crawler.fetch_comments_from_booking',
                        'crawler.fetch_comments_from_airbnb'])
