import email
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from database import schema,models,databases,crud
from database.databases import Base, engine
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/user/me", response_model=schema.User)
async def read_user_me(current_user : schema.User = Depends()):
    return current_user

@router.post("/user/register")
async def register(
    db : Session = Depends(databases.get_db),
    user_create : schema.UserCreate = Depends(),
    ):
    try:
        crud.create_user(db=db, user = user_create)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please retry register"
        )
        
    return status.HTTP_201_CREATED

@router.post("/login")
async def login(
    users : schema.UserLogin = Depends()
):
    try:
        user = models.User.get(email=users.email)
        print(user)
        if user is None:
            raise Exception
        checkpassword =bcrypt.checkpw(users.password.encode('utf-8'), user.password.encode('utf-8'))
        print(checkpassword)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="None!"
        )
    