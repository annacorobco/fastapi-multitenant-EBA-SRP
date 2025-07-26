from uuid import UUID

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.exceptions import DoesNotExist

from app.db.core import init_core_db
from app.db.models.core_models import Organization
from app.db.tenant import init_tenant_db


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tenant_id = request.headers.get("X-TENANT")
        await init_core_db()

        if tenant_id:
            try:
                tenant_uuid = UUID(tenant_id)
            except ValueError:
                # Explicitly ensure the client receives proper JSON error messages
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid X-TENANT format. Must be a valid UUID."},
                )
            try:
                # Ensure we fetch tenant from the CORE DB
                tenant = await Organization.get(id=tenant_uuid)
                await init_tenant_db(tenant.db_name)
                request.state.tenant = tenant
            except DoesNotExist:
                return JSONResponse(
                    status_code=404,
                    content={"detail": "Tenant not found"},
                )
        else:
            request.state.tenant = None  # Core DB usage

        return await call_next(request)
