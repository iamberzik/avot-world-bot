import os

from redis import Redis
from rq import Queue

from core.globals import ENV_REDIS_HOST_KEY, ENV_REDIS_PORT_KEY

redis_host = os.getenv(ENV_REDIS_HOST_KEY)
redis_port = os.getenv(ENV_REDIS_PORT_KEY)
redisQueue = Queue(connection=Redis(host=redis_host, port=redis_port))
