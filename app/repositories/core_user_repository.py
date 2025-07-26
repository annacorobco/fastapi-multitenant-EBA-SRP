from app.db.models.core_models import CoreUser


class CoreUserRepository:
    async def get_by_email(self, email: str):
        return await CoreUser.get_or_none(email=email)

    async def get_by_id(self, user_id: str):
        return await CoreUser.get_or_none(id=user_id)

    async def create(self, email: str, password: str, is_owner: bool):
        return await CoreUser.create(email=email, hashed_password=password, is_owner=is_owner)

    async def update_name(self, user_id: str, full_name: str):
        user = await CoreUser.get(id=user_id)
        user.full_name = full_name
        await user.save()
        return user
