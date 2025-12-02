

# REDIS
docker run -p 6379:6379 redis
docker run -d --name redis -p 6379:6379 redis
redis           name of the image to download & run
-d              detached mode
--name redis    gives a name for easier terminal operations


# WORKER
python -m celery -A celery_app worker -P solo
python -m celery -A celery_app worker -P solo --loglevel=info
-A celery_app       path to celery app with Celery object
worker              subcommand - this code is of a worker
-P solo             windows workaround



# PRODUCER
python producer.py