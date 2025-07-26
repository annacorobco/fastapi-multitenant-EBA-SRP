from fastapi import APIRouter, Depends, HTTPException, Header, Request

from app.repositories.tenant_repository import TenantUserRepository
from app.services.auth_service import AuthService
from app.services.tenant_user_service import TenantUserService
from app.schemas.request_schemas import RegisterTenantUserRequest, \
    LoginTenantUserRequest, UpdateTenantUserRequest
from app.schemas.response_schemas import TenantUserRegisterResponse, \
    TenantUserLoginResponse, TenantUserProfileResponse


tenant_user_service = TenantUserService(TenantUserRepository())
public_tenant_router = APIRouter(dependencies=[Depends(AuthService.require_tenant_header)])
auth_tenant_router = APIRouter(dependencies=[Depends(AuthService.require_tenant_header),
                                             Depends(AuthService.get_current_user)])


@public_tenant_router.post("/api/tenant/auth/register", response_model=TenantUserRegisterResponse)
async def register_tenant_user(data: RegisterTenantUserRequest):
    user = await tenant_user_service.user_exists(email=data.email)
    if user:
        raise HTTPException(400, "User already exists")
    user = await tenant_user_service.create_user(
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name
    )

    return user


@public_tenant_router.post("/api/tenant/auth/login", response_model=TenantUserLoginResponse)
async def login_tenant_user(data: LoginTenantUserRequest, request: Request):
    user = await tenant_user_service.user_exists(email=data.email)
    if not user or not AuthService.verify_password(
            plain=data.password,
            hashed=user.hashed_password
            ):
        raise HTTPException(401, "Invalid credentials")
    token = AuthService.create_access_token({
        "sub": str(user.id),
        "tenant": str(request.state.tenant.id),
        "scope": "tenant"
    })

    return TenantUserLoginResponse(access_token=token)


@auth_tenant_router.get("/api/tenant/users/me", response_model=TenantUserProfileResponse)
async def get_tenant_user_profile(request: Request):
    if request.state.scope != "tenant":
        raise HTTPException(403, "Only tenant users can access this endpoint")

    return request.state.tenant_user


@auth_tenant_router.put("/api/tenant/users/me", response_model=TenantUserProfileResponse)
async def update_tenant_user_profile(data: UpdateTenantUserRequest, request: Request):
    if request.state.scope != "tenant":
        raise HTTPException(403, "Only tenant users can update their profile")

    user = await tenant_user_service.update_user(user=request.state.tenant_user,
                                                 data=dict(data))

    return user
