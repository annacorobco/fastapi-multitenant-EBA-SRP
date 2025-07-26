from tortoise import fields
from tortoise.models import Model


class CoreUser(Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(255, unique=True)
    hashed_password = fields.CharField(255)
    is_owner = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Organization(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(255, unique=True)
    db_name = fields.CharField(255, unique=True)
    owner = fields.ForeignKeyField("models.CoreUser", related_name="organizations")
    created_at = fields.DatetimeField(auto_now_add=True)
