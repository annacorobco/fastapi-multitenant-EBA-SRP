from passlib.context import CryptContext

from app.events.base_event import EventDispatcher
from app.events.core_user_events import CoreUserCreatedEvent
from app.repositories.core_user_repository import CoreUserRepository
from app.services.auth_service import AuthService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class CoreUserService:
    def __init__(self, user_repo: CoreUserRepository):
        self.core_user_repo = user_repo

    async def user_exists(self, email: str):
        return await self.core_user_repo.get_by_email(email=email)

    async def create_user(self, email: str, password: str, is_owner: bool):
        user = await self.core_user_repo.create(email, AuthService.get_password_hash(password), is_owner)
        await EventDispatcher.publish(CoreUserCreatedEvent(user.id, email, is_owner))
        return user

    async def update_profile(self, user_id: str, full_name: str):
        return await self.core_user_repo.update_name(user_id, full_name)
