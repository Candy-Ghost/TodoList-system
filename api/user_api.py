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

class login_user_password(BaseModel):
    username: str
    password: int=123456

class uppass (BaseModel):
    username: str
    password:int
    email: str

    @field_validator("password")
    def validate_password(cls, value: int) -> int:
        if not (100000 <= value <= 999999999):
            raise ValueError("密码6-9位")
        return value  # 可以修改值


@user_api.post("/enroll",summary="注册接口")
async def enrolluser(enroll:enrollin):
    existing_user = await Users.filter(username=enroll.username).first()
    if existing_user:
        return {"操作": "用户名已存在"}
    #filter() → 总是返回查询集（可能为空），不报错。
    #get() → 如果找不到记录或找到多条记录，会抛出异常
    # 然后查询邮箱是否已存在
    existing_email = await Users.filter(email=enroll.email).first()
    if existing_email:
        return {"操作": "email已存在"}

    # 如果用户名和邮箱都不存在，则创建新用户
    adduser = await Users.create(
        username=enroll.username,
        password=enroll.password,
        email=enroll.email
    )
    return {"操作": "添加一个账号"}





@user_api.post("/login",summary="登入接口")
async def login_user(account:login_user_password):
    user = await Users.filter(username=account.username).first()

    if not user:
        return {"操作": "账号为空"}


    # 用户名存在，检查密码是否正确
    correct_user_password = await Users.filter(
        username=account.username,
        password=account.password
    ).first()

    if not correct_user_password  :
        return {"操作": "密码错误"}

    # 用户名和密码都正确，生成token
    data = {"username": account.username}
    token = create_token(data)
    return token



@user_api.put("/uppass",summary="修改密码")
async def update_passwode(up_password:uppass):
    user = await Users.filter(username=up_password.username).first()
    if not user:
        return {"操作": "修改失败，账号不存在"}

    if user.email != up_password.email:
        return {"操作": "修改失败，邮箱不匹配"}

    update_data = up_password.dict(exclude_unset=True)

    updated_rows = await Users.filter(
        username=up_password.username,
        email=up_password.email
    ).update(**update_data)

    if updated_rows > 0:
        return {"操作": "修改成功"}
    else:
        return {"操作": "修改失败，请检查数据是否有效"}


# @user_api.get("/get_token")
# async def get_token(date=Depends(verify_token)):
#     return date