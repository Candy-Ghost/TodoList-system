from pydantic import BaseModel, field_validator
from datetime import datetime

class Add_todo (BaseModel):
    title:str
    content: str
    state:str="未完成"
    # @field_validator("password")
    # def validate_password(cls, value: int) -> int:
    #     if not (100000 <= value <= 999999999):
    #         raise ValueError("密码6-9位")
    #     return value  # 可以修改值

class Update_todo (BaseModel):
    title: str
    content: str
    updated:str=datetime.now()
    state: str = "未完成"
