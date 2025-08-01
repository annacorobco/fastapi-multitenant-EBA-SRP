from app.db.models.tenant_models import TenantUser
from app.dependencies import redis_cache, rabbitmq_broker
from app.events.base_event import EventDispatcher
from app.events.tenant_user_events import TenantUserCreatedEvent, TenantUserUpdatedEvent
from app.repositories.tenant_repository import TenantUserRepository
from app.services.auth_service import AuthService
from app.logger import logger


class TenantUserService:
    def __init__(self, user_repo: TenantUserRepository):
        self.tenant_user_repo = user_repo
        self.cache = redis_cache
        self.publisher = rabbitmq_broker

    async def user_exists(self, email: str):
        return await self.tenant_user_repo.get_by_email(email=email)

    async def create_user(self, email: str, password: str, first_name: str, last_name: str):
        user = await self.tenant_user_repo.create(
            email=email,
            hashed_password=AuthService.get_password_hash(password),
            first_name=first_name,
            last_name=last_name)
        try:
            await self.cache.set(f"user:{user.id}", user.email)
        except Exception as e:
            pass
        try:
            event = TenantUserCreatedEvent(
                user_id=user.id, email=email, first_name=first_name, last_name=last_name
            )
            await self.publisher.publish(event.dict())
        except Exception as e:
            logger.exception(f"[Create User Error] {e}")

        return user

    async def update_user(self, user: TenantUser, data: dict):
        for field, value in data.items():
            if value:
                setattr(user, field, value)
        await user.save()
        await EventDispatcher.publish(TenantUserUpdatedEvent(user.id))

        return user



