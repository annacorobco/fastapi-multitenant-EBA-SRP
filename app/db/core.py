from tortoise import Tortoise

from app.config import settings


TORTOISE_ORM_CORE = {
    "connections": {
        "default": settings.CORE_DB_URL
    },
    "apps": {
        "models": {
            "models": ["app.db.models.core_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_core_db():
    await Tortoise.init(db_url=settings.CORE_DB_URL, modules={"models": ["app.db.models.core_models"]})
    await Tortoise.generate_schemas()
