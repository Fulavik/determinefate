from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(max_length=4)
    uid = fields.BigIntField(max_length=20, pk=True)

    language = fields.IntField(max_length=2)

    class Meta: 
        table = 'users'