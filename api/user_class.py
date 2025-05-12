from pydantic import BaseModel, field_validator
from fastapi.exceptions import HTTPException

class Enrollin(BaseModel):
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

class Login_user_password(BaseModel):
    username: str
    password: int=123456

class Updatepass (BaseModel):
    username: str
    password:int
    email: str

    @field_validator("password")
    def validate_password(cls, value: int) -> int:
        if not (100000 <= value <= 999999999):
            raise ValueError("密码6-9位")
        return value  # 可以修改值
