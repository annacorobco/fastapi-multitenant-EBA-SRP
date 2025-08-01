import os

from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
REDIS_URL = os.environ.get('REDIS_URL')

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=REDIS_URL
)

celery_app.conf.task_routes = {
    "handle_user_created": {"queue": "user_created"},
}
celery_app.autodiscover_tasks(["app.services.tasks"])
