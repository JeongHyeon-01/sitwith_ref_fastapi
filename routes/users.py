from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie 
from database import schema,models,databases,crud
from database.databases import Base, engine
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=schema.User)
async def read_user_me(current_user : schema.User = Depends()):
    return current_user

@router.post("/register")
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
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    # users : schema.UserLogin = Depends(),
    db : Session = Depends(databases.get_db),
):
    try:
        user = crud.authenticate_user(db = db, email = form_data.email, password = form_data.password)
        if not user:
            raise Exception
        
        access_token_expires = timedelta(minutes=int(crud.token_expire))

        access_token = crud.create_access_token(data={
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
            "is_activate" : user.is_activate
            }, expires_delta= access_token_expires)

        response.set_cookie(key = "access_token", value=access_token, secure=True, httponly=True)
        return status.HTTP_200_OK
        
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
        
@router.post("/token")
async def token(
    response: Response,
    access_token : Optional[str] = Cookie(None),
    token: str = Depends(oauth2_scheme)
):
    try:
        access_token = crud.refresh_access_token(access_token)
        response.set_cookie(key = "access_token", value=access_token, secure=True, httponly=True)
        return status.HTTP_200_OK
    
    except Exception as e:
        return HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )