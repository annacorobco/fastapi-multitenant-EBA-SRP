from tortoise import Tortoise

from app.config import settings

TORTOISE_ORM_TENANT = {
    "connections": {
        "default": settings.DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ["app.tenant.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_tenant_db(db_name: str):
    tenant_url = f"{settings.DATABASE_URL}/{db_name}"
    await Tortoise.init(db_url=tenant_url, modules={"models": ["app.db.models.tenant_models"]})
    await Tortoise.generate_schemas()
