from sre_constants import SUCCESS
import bcrypt
from sqlalchemy.orm import Session
from database import models,schema
from database import schema
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from core.validator import validate_email,validate_username, validate_password
load_dotenv()

secretkey = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

def get_user(db : Session, user_id : int):
    return db.query(models.User).filter(models.User.email == user_id).first()

def get_user_by_username(db : Session, username : str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db : Session, email : str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db : Session, skip : int = 0, limit : int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user(db : Session, user : schema.UserCreate):
    db_user = models.User(
        email = validate_email(user.email),
        username = validate_username(user.username),
        password = get_password_hash(validate_password(user.password))
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return SUCCESS

class UserInDB(schema.User):
    hashed_password: str

def get_user(db, email : str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validation_password(origin_password, check_password):
    if origin_password == check_password:
        return origin_password
    else:
        return None

def verify_password(plan_password, hashd_password):
    return pwd_context.verify(plan_password, hashd_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, email: str, password: str):
    user = db.get(email = email)
    is_verrified = bcrypt.checkpw(db.password.encode('utf-8'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+ expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, secretkey, algorithms = algorithm)
    return encoded_jwt