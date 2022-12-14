from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email : str

class UserCreate(UserBase):
    username : str
    password : str
    check_password : str
        
class User(UserBase):
    username : str

class UserLogin(UserBase):
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id : int
    username: str | None = None