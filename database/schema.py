from pydantic import BaseModel
from typing import Optional

class ResponseUser(BaseModel):
    id : int
    username : str
    password : str
    email : str
    is_activate : Optional[bool] = None

    class Config:
        orm_mode = True
        
        
class RequestUser(BaseModel):
    username : str
    password : str
    email : str