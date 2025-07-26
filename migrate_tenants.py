import asyncio
from aerich import Command
from tortoise import Tortoise

from app.db.models.core_models import Organization
from app.db.core import TORTOISE_ORM_CORE


async def get_all_tenants():
    """Fetch all tenant databases from the core database."""
    await Tortoise.init(config=TORTOISE_ORM_CORE)
    tenants = await Organization.all().values("id", "db_name")
    await Tortoise.close_connections()
    return tenants


async def migrate_tenant(db_name: str):
    """Run Aerich migrations for a specific tenant database."""
    tortoise_config = {
        "connections": {"default": f"postgres://postgres:pass@db:5432/{db_name}"},
        "apps": {
            "models": {
                "models": ["app.tenant.models", "aerich.models"],
                "default_connection": "default",
            }
        },
    }

    print(f"Running migrations for tenant DB: {db_name}")

    command = Command(tortoise_config, app="models", location="migrations_tenant")
    await command.init()
    await command.upgrade()  # applies migrations


async def migrate_all_tenants():
    tenants = await get_all_tenants()
    for tenant in tenants:
        await migrate_tenant(tenant["db_name"])


if __name__ == "__main__":
    asyncio.run(migrate_all_tenants())
