from pydantic import BaseModel
from typing import List, Optional, Union

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
    
class CategoryBase(BaseModel):
    id : int | None = None
    title : str
    
    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    title : str
    
class ProductBase(BaseModel):
    name : str
    price : float
    description : str

class ProductCreate(ProductBase):
    category_id : int
    
    class Config:
        orm_mode = True

class ColorBase(BaseModel):
    name: str
    
class ColorCreate(ColorBase):
    pass

class ProductColorBase(BaseModel):
    inventory : int

class ProductColorCreate(ProductColorBase):
    color : int
    product_id : int
    class Config:
        orm_mode = True