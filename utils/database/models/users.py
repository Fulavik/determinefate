from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(max_length=4, pk=True)
    uid = fields.BigIntField(max_length=20)

    language = fields.IntField(max_length=2)

    class Meta: 
        table = 'users'