from fastapi import APIRouter, Form, Depends, HTTPException
from pydantic import BaseModel, field_validator
from JWTYZ import create_token,verify_token
from api.user_api import user_api
from models import *
from datetime import datetime
index_api=APIRouter()
def get_token(date=Depends(verify_token)):
    print(date)
    return date
@index_api.get("/",summary="主界面接口")
async def get_index(username: dict = Depends( get_token)):
    # return username
    print(username['username'])
    user = await Users.get(username=username['username'])
    user_id = user.id
    tasks_data = await Tasks.filter(users_id=user_id ).values("title", "content","created_at","state")
    # result = []
    # for datas in tasks_data:
    #     user = await Users.get(id=datas["users_id"])
    #     result.append({
    #         "username": user.username,
    #         "title": datas["title"],
    #         "content": datas["content"]
    #     })
    return tasks_data


class add_todo (BaseModel):
    title:str
    content: str
    state:str="未完成"
    # @field_validator("password")
    # def validate_password(cls, value: int) -> int:
    #     if not (100000 <= value <= 999999999):
    #         raise ValueError("密码6-9位")
    #     return value  # 可以修改值


@index_api.post("/add", summary="添加todo")
async def add_todo(todo_data: add_todo,username: dict = Depends(get_token)  # 确保返回 {'username': 'xxx'}
):
    try:
        # 1. 获取用户id
        user = await Users.get(username=username['username'])
        print(user.id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 2.
        await Tasks.create(
            users_id=user.id,
            title=todo_data.title,
            content=todo_data.content,
            state=todo_data.state
        )

        return {"操作": "添加成功"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class up_todo (BaseModel):
    title: str
    content: str
    updated:str=datetime.now()
    state: str = "未完成"

@index_api.put("/uptodo/{id1}",summary="修改todo")
async def update_todo(id1,up_Todo:up_todo,username: dict = Depends(get_token)):
    try:
        user= await Users.get(username=username['username'])
        user_id=user.id
        print(user_id)
        data = up_Todo.dict()
        print(data)
        await Tasks.filter(id=id1,users_id=user.id,).update(**data)
        return {"操作": "修改成功"}
    except:
        return {"操作": "修改失败"}

@index_api.delete("/del/{todo_id}",summary="删除todo")
async def del_todo(todo_id:int,username: dict = Depends(get_token)):
    try:
        user = await Users.get(username=username['username'])
        user_id = user.id
        deletete_todo= await Tasks.filter(users_id=user_id,id=todo_id).delete()
        return {"操作": "删除成功"}
    except:
        return{"操作": "删除失败"}

@index_api.get("/finish",summary="显示已完成的todo")
async def ture_finish(username: dict = Depends(get_token)):
    # return username
    print(username['username'])
    user = await Users.get(username=username['username'])
    user_id = user.id
    finish= await Tasks.filter(users_id=user_id,state="已完成").values("title", "content","created_at")
    return finish

@index_api.get("/NO_finish",summary="显示未完成的todo")
async def NO_finish(username: dict = Depends(get_token)):
    # return username
    print(username['username'])
    user = await Users.get(username=username['username'])
    user_id = user.id
    no_finish = await Tasks.filter(users_id=user_id, state="未完成").values("title", "content","created_at")
    return no_finish