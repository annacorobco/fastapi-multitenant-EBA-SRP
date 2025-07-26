from app.db.models.tenant_models import TenantUser
from app.events.base_event import EventDispatcher
from app.events.tenant_user_events import TenantUserCreatedEvent, TenantUserUpdatedEvent
from app.repositories.tenant_repository import TenantUserRepository
from app.services.auth_service import AuthService


class TenantUserService:
    def __init__(self, user_repo: TenantUserRepository):
        self.tenant_user_repo = user_repo

    async def user_exists(self, email: str):
        return await self.tenant_user_repo.get_by_email(email=email)

    async def create_user(self, email: str, password: str, first_name: str, last_name: str):
        user = await self.tenant_user_repo.create(
            email=email,
            hashed_password=AuthService.get_password_hash(password),
            first_name=first_name,
            last_name=last_name)
        await EventDispatcher.publish(TenantUserCreatedEvent(user.id, email, first_name, last_name))

        return user

    async def update_user(self, user: TenantUser, data: dict):
        for field, value in data.items():
            if value:
                setattr(user, field, value)
        await user.save()
        await EventDispatcher.publish(TenantUserUpdatedEvent(user.id))

        return user



