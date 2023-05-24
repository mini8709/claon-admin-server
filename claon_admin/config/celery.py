from celery import Celery
from claon_admin.config.config import conf

broker = "amqp://claon_user:claon_password@127.0.0.1:5672"
backend = "redis://127.0.0.1:6379"

celery_client = Celery(
    "claon",
    # broker=conf().CELERY_BROKER,
    broker=broker,
    # backend="redis://{redis_host}:{redis_port}".format(
    #     redis_host=conf().REDIS_HOST,
    #     redis_port=conf().REDIS_PORT,
    # )
    backend=backend,
)


@celery_client.task()
def test_task():
    print(111)
