import asyncpg

from app.config import settings
from app.db.models.core_models import Organization
from app.db.models.tenant_models import TenantUser


class OrganizationRepository:
    async def create(self, name: str, db_name: str, owner_id: int):
        return await Organization.create(
            name=name,
            db_name=db_name,
            owner_id=owner_id
        )

    async def create_tenant_db(self, db_name: str):
        conn = await asyncpg.connect(settings.CORE_DB_URL)
        try:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
        finally:
            await conn.close()

    async def get_by_name(self, name: str):
        return await Organization.exists(name=name)

    async def delete_by_id(self, org_id: int):
        return await Organization.filter(id=org_id).delete()


class TenantUserRepository:
    async def get_by_email(self, email: str):
        return await TenantUser.get_or_none(email=email)

    async def create(self, email: str,
                     hashed_password: str,
                     first_name: str = None,
                     last_name: str = None):
        return await TenantUser.create(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )


