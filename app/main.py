from fastapi import FastAPI

from app.dependencies import redis_cache, rabbitmq_broker
from app.middleware.tenant_middleware import TenantMiddleware
from app.routers.core_routers import public_core_router, auth_core_router
from app.routers.tenant_routers import public_tenant_router, auth_tenant_router


app = FastAPI(
    title="Multi-Tenant FastAPI Event-Based and Service-Repository Pattern",
    version="1.0.0",
    description="Multi-tenant platform with core & tenant authentication",
)


@app.on_event("startup")
async def startup():
    await redis_cache.connect()
    await rabbitmq_broker.connect()


@app.on_event("shutdown")
async def shutdown():
    await redis_cache.close()
    if rabbitmq_broker.connection:
        await rabbitmq_broker.connection.close()

# Add Tenant Middleware
app.add_middleware(TenantMiddleware)

# Include Core & Tenant Routers
app.include_router(public_core_router)
app.include_router(auth_core_router)
app.include_router(public_tenant_router)
app.include_router(auth_tenant_router)
