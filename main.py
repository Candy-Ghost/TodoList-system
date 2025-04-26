from fastapi import FastAPI
import uvicorn
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from api.user_api import user_api
from api.index_api import index_api

app=FastAPI()

app.include_router(user_api,tags=['账号管理api接口'],)
app.include_router(index_api,prefix="/user",tags=['主页接口'],)
    #mysql
register_tortoise(
    app=app,
    config=TORTOISE_ORM,


)


if __name__ == '__main__':
    uvicorn.run("main:app",port=8000,reload=True)

    # aerich init -t settings.TORTOISE_ORM 初始化配置
    #aerich init-db  初始化数据库（一般只用一次）
    #aerich migrate[--name] 更改数据库
    #aerich upgrade 确定更改
    #aerich aerich upgrade 返回上一次更改

