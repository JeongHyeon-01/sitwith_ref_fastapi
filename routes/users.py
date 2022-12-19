from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie 
from database import schema,models,databases,crud
from database.databases import Base, engine
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.log import LOG

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=schema.User)
async def read_user_me(current_user : schema.User = Depends()):
    return current_user

@router.post("/register")
async def register(
    user_create : schema.UserCreate,
    db : Session = Depends(databases.get_db),
    # user_create : schema.UserCreate = Depends(),
    
    ):
    try:
        crud.create_user(db=db, user = user_create)
    except Exception as e:
        LOG.error(str(e))
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please retry register" + str(e) 
        )
        
    return status.HTTP_201_CREATED

@router.post("/login")
async def login(
    response: Response,
    users : schema.UserLogin,
    db : Session = Depends(databases.get_db),
):
    try:
        user = crud.authenticate_user(db = db, email = users.email, password = users.password)
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
        LOG.error("UNAUTHORIZE" if str(e) is None else str(e))
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZE" if str(e) is None else str(e)
        )
        
@router.post("/token")
async def token(
    response: Response,
    access_token : Optional[str] = Cookie(None),
):
    try:
        access_token = crud.refresh_access_token(access_token)
        response.set_cookie(key = "access_token", value=access_token, secure=True, httponly=True)
        LOG.success(f"User [{crud.decode_access_token(access_token)['username']}] token refreash complete")
        return Response(
            status_code=status.HTTP_200_OK,
            content= str(datetime.fromtimestamp(crud.decode_access_token(access_token)['exp']))
        )

    except Exception as e:
        LOG.error(str(e))
        return HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= str(e) 
        )
        
@router.post('/logout')
async def logout(
    response : Response,
    access_token : Optional[str] = Cookie(None),
):
    try:
        response.delete_cookie(key="access_token", value = access_token ,secure=True,httponly=True)
    
    except Exception as e:
        LOG.error(str(e))
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )  