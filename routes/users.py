from fastapi import APIRouter, Depends, HTTPException, status
from database import schema,models,databases,crud

from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/user/me", response_model=schema.User)
async def read_user_me(current_user : schema.User = Depends()):
    return current_user

@router.post("/user/register", response_model=schema.User)
async def register(
    db : Session = Depends(databases.get_db),
    user_create : schema.UserCreate = Depends(),
    ):
    # password = crud.validation_password(user_create.password, user_create.check_password)
    # if password == None:
        # return "None"
    db_user = models.User(
        email = user_create.email,
        username = user_create.username,
        password = crud.get_password_hash(crud.validation_password(user_create.password, user_create.check_password))
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)        
    return user_create  
# @router.post("/login")
# async def login():
#   pass