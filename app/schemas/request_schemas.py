from typing import Optional

from pydantic import BaseModel, EmailStr


# Core User
class RegisterCoreUserRequest(BaseModel):
    email: EmailStr
    password: str


class LoginCoreUserRequest(BaseModel):
    email: EmailStr
    password: str


class CreateOrganizationRequest(BaseModel):
    name: str


# Tenant User
class RegisterTenantUserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class LoginTenantUserRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateTenantUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

