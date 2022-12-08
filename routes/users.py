from fastapi import APIRouter, Depends, HTTPException, status
from database import schema,models,databases,crud
from database.databases import Base, engine
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
    db_user = crud.create_user(db=db, user = user_create)
    return db_user.__dict__

# @router.post("/login")
# async def login():
#   pass