from tortoise import fields
from tortoise.models import Model


class TenantUser(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True)
    hashed_password = fields.CharField(255)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

