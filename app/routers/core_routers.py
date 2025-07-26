from fastapi import APIRouter, Depends, HTTPException, Request

from app.repositories.core_user_repository import CoreUserRepository
from app.schemas.request_schemas import RegisterCoreUserRequest, \
    LoginCoreUserRequest, CreateOrganizationRequest
from app.schemas.response_schemas import CoreUserRegisterResponse, \
    CoreUserLoginResponse, OrganizationResponse
from app.services.core_user_service import CoreUserService
from app.services.tenant_onboarding_service import TenantOnboardingService
from app.services.auth_service import AuthService

core_user_service = CoreUserService(CoreUserRepository())
public_core_router = APIRouter()
auth_core_router = APIRouter(dependencies=[Depends(AuthService.get_current_user)])


@public_core_router.post("/api/core/auth/register", response_model=CoreUserRegisterResponse)
async def register_core_user(data: RegisterCoreUserRequest):
    user = await core_user_service.user_exists(email=data.email)
    if user:
        raise HTTPException(400, "User already exists")
    user = await core_user_service.create_user(
        email=data.email,
        password=data.password,
        is_owner=True
    )

    return user


@public_core_router.post("/api/core/auth/login", response_model=CoreUserLoginResponse)
async def login_core_user(data: LoginCoreUserRequest):
    user = await core_user_service.user_exists(email=data.email)
    if not user or not AuthService.verify_password(
            plain=data.password,
            hashed=user.hashed_password
            ):
        raise HTTPException(401, "Invalid credentials")
    token = AuthService.create_access_token({"sub": str(user.id), "scope": "core"})

    return CoreUserLoginResponse(access_token=token)


@auth_core_router.post("/api/core/organizations", response_model=OrganizationResponse)
async def create_organization(data: CreateOrganizationRequest, request: Request):
    if not request.state.core_user.is_owner:
        raise HTTPException(status_code=403, detail="Only owners can create organizations.")

    service = TenantOnboardingService(name=data.name, current_user=request.state.core_user)
    organization = await service.create()

    return organization
