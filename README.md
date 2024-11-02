# Distributed_Crawler

Python version: 3.9.6
Rabbitmq 3.13.3 with management component

Change broker_url = 'pyamqp://guest:guest@localhost:30001/crawler' in crawler/celery_config.py to your Rabbitmq address, 
the structure is 'pyamqp://Rabbitmq-username:Rabbitmq-password@Rabbitmq-host-ip:Rabbitmq-port/Rabbitmq-virtual-host'

The system must setup on Linux, use pyenv or something else to create a virtual environment.
After the venv is activated 
Run: 
 "pip install -r requirements.txt" in root directory of this project.

Linux:
After all finished, run "celery -A crawler.celery_app worker --loglevel=info" to start standalone mode.
Run:
 "celery -A crawler.celery_app worker --loglevel=info --autoscale=10,3 --hostname=worker1@%h.%n &
  celery -A crawler.celery_app worker --loglevel=info --autoscale=10,3 --hostname=worker2@%h.%n &
  celery -A crawler.celery_app worker --loglevel=info --autoscale=10,3 --hostname=worker3@%h.%n"
to start 3 pods.
If more pods wanted, just add more "celery -A crawler.celery_app worker --loglevel=info --autoscale=max,min --hostname=hostname" into command lines
Replace "max" and "min" with an integer, the number must >0, change hostname to whatever you want and take care about hostname conflicts in you command.

If you want to shut down all celery pods
Run
 "celery -A crawler control shutdown" to shut all pod down.
