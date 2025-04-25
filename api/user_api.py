from fastapi import APIRouter,Form,Depends
from models import *
from pydantic import BaseModel, field_validator
from fastapi import Request
from fastapi.exceptions import HTTPException
from JWTYZ import create_token,verify_token

user_api=APIRouter()

class enrollin(BaseModel):
    username :str
    password : int
    email : str

    @field_validator("password")
    def validate_password(cls, value: int) -> int:
        if not (100000 <= value <= 999999999):
            raise HTTPException(
                status_code=400,
                detail="密码6-9位"
            )
        return value  # 可以修改值

    @field_validator("email")
    def validator_email(cls, value: str) -> str:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise HTTPException(
                status_code=400,
                detail="无效的电子邮件格式"
            )
        return value

    # @field_validator("password")
    # def validate_password(cls, value: int) -> int:
    #     if not (100000 <= value <= 999999999):
    #         raise ValueError("密码6-9位")
    #     return value  # 可以修改值

@user_api.post("/enroll",summary="注册接口")
async def enrolluser(enroll:enrollin):

    try:
        new_user = await Users.get(username=f"{enroll.username}")
        return {"操作": "用户名已存在"}
    except:
        try:
            you_email = await Users.get(email=f"{enroll.email}")
            return {"操作": "email已存在"}
        except:
            adduser = await Users.create(
                username=enroll.username,
                password=enroll.password,
                email=enroll.email
            )
            return {"操作": "添加一个账号"}
class login_user_password(BaseModel):
    username: str
    password: int=123456




@user_api.post("/login",summary="登入接口")
async def login_user(password:login_user_password):
    try:
        cyun = await Users.get(username=f"{password.username}")
        try:
            yun = await Users.get(username=f"{password.username}", password=f"{password.password}")
            # print(yun.email)
            # y_id=yun.id
            data = {"username":password.username}
            token = create_token(data)
            return token

        except:
            return {"操作": "账号或密码错误"}

    except:
        return {"操作": "账号为空"}

class uppass (BaseModel):
    username: str
    password:int
    email: str

    @field_validator("password")
    def validate_password(cls, value: int) -> int:
        if not (100000 <= value <= 999999999):
            raise ValueError("密码6-9位")
        return value  # 可以修改值

@user_api.put("/uppass",summary="修改密码")
async def update_passwode(up_passwode:uppass):
    try:
        update_pass = await Users.get(username=f"{up_passwode.username}")
        data = up_passwode.dict()
        print(data)
        await Users.filter(username=up_passwode.username,email=up_passwode.email).update(**data)
        return {"操作": "修改成功"}
    except:
        return {"操作": "修改失败,请检查账号或邮箱是否正确"}


# @user_api.get("/get_token")
# async def get_token(date=Depends(verify_token)):
#     return date