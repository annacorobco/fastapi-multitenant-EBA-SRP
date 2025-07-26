from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.db.models.core_models import CoreUser
from app.db.models.tenant_models import TenantUser
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = APIKeyHeader(name="Authorization")


class AuthService:
    @staticmethod
    def verify_password(plain, hashed):
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    async def get_current_user(
            request: Request,
            token: str = Depends(bearer_scheme),
            x_tenant: str = Header(None),
    ):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            tenant_id = payload.get("tenant")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Core users (no tenant in token)
        if not tenant_id:
            user = await CoreUser.get_or_none(id=user_id)
            if not user or not user.is_owner:
                raise HTTPException(403, "Not authorized to access core data")
            scope = "core"
            request.state.core_user = user
            request.state.scope = scope
            return {"scope": "core", "user": user}

        # Tenant users (verify token tenant matches header)
        if x_tenant != tenant_id:
            raise HTTPException(403, detail="Tenant mismatch")

        user = await TenantUser.get_or_none(id=user_id)
        if not user:
            raise HTTPException(401, "Tenant user not found")
        scope = "tenant"
        request.state.tenant_user = user
        request.state.tenant_id = tenant_id
        request.state.scope = scope
        return {"scope": "tenant", "tenant_id": tenant_id, "user": user}

    @staticmethod
    async def require_tenant_header(x_tenant: UUID = Header(...)):
        if not x_tenant:
            raise HTTPException(status_code=400, detail="X-TENANT header is required")

        return x_tenant
