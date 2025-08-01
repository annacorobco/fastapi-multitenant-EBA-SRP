from app.events.user_events import TenantUserCreatedEvent
from app.worker import celery_app

from app.logger import logger


@celery_app.task(name="handle_user_created")
def handle_user_created(data):
    try:
        event = TenantUserCreatedEvent(**data)
        logger.info(f"[Celery] Processing new user: {event.email}")
    except Exception as e:
        logger.exception(f"[Celery Error] {e}")
