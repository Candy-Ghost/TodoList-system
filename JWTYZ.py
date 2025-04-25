

import jwt
from  datetime import  datetime,timedelta,timezone
import secrets
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY=secrets.token_hex(32)
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")
def create_token(data:dict):

    to_encode=data.copy()
    to_encode.update({"exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    encode_jwt=jwt.encode(
        to_encode,#要通过token传输的内容
        SECRET_KEY,#JWT签名的密钥
        algorithm=ALGORITHM,#JWT签名的算法
    )
    return encode_jwt

def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token已过期",
            headers={"WWW-Authenticate":"Bearer"}
        )
    return payload
