from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction

from app.db.tenant import init_tenant_db
from app.db.models.tenant_models import TenantUser
from app.repositories.tenant_repository import OrganizationRepository, TenantUserRepository
from app.logger import logger


class TenantOnboardingService:
    def __init__(self, name: str, current_user: TenantUser):
        self.name = name
        self.current_user = current_user
        self.org_repo = OrganizationRepository()
        self.tenant_repo = TenantUserRepository()

    async def create(self):
        db_name = f"tenant_{self.name.lower()}"
        owner_id = str(self.current_user.id)
        # Ensure unique org name
        if await self.org_repo.get_by_name(name=self.name):
            raise HTTPException(
                status_code=400,
                detail=f"Organization '{self.name}' already exists."
            )

        # Create organization entry inside a core DB transaction
        try:
            async with in_transaction():
                org = await self.org_repo.create(
                    name=self.name,
                    db_name=db_name,
                    owner_id=owner_id
                )
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Could not create organization. Check if owner exists."
            )

        # After the core DB transaction commits, create the tenant DB
        try:
            await self.org_repo.create_tenant_db(db_name=db_name)
            await init_tenant_db(db_name)
            await self.tenant_repo.create(email=self.current_user.email,
                                          hashed_password=self.current_user.hashed_password)
            logger.info("Tenant DB was initialized")
            return org
        except Exception as e:
            logger.exception(e)
            # rollback org entry if tenant DB creation fails
            await self.org_repo.delete_by_id(org_id=org.id)
            raise HTTPException(
                status_code=500,
                detail=f"Tenant database creation failed: {str(e)}"
            )
