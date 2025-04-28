from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=500,unique=True, description="账号名")
    password = fields.CharField(max_length=500, description="密码")
    email = fields.CharField(max_length=500,unique=True, description="邮件")
    created_at = fields.DatetimeField(auto_now_add=True)


class Tasks(Model):
    id = fields.IntField(pk=True)
    users_id=fields.IntField(max_length=500)
    title= fields.CharField(max_length=500, description="标题")
    content = fields.CharField(max_length=1000, description="内容")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated = fields.CharField(max_length=200, null=True,description="更改的时间")
    state= fields.CharField(max_length=50, description="状态")