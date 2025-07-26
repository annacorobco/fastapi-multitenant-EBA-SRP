from uuid import UUID

from pydantic import BaseModel, EmailStr


# Core Users
class CoreUserRegisterResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_owner: bool

    class Config:
        orm_mode = True


class CoreUserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrganizationResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True


# Tenant Users
class TenantUserRegisterResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class TenantUserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TenantUserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True
