from arq.connections import RedisSettings
from service.workers.simple_worker import simple_work


class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(host='localhost', port=6379)
