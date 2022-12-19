from sre_constants import SUCCESS
import bcrypt
from sqlalchemy.orm import Session
from database import models,schema,databases
from database import schema
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from core.validator import validate_email,validate_username, validate_password
load_dotenv()

secretkey = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expire = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
def get_user(db : Session, user_id : int):
    return db.query(models.User).filter(models.User.email == user_id).first()

def get_user_by_username(db : Session, username : str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db : Session, email : str):
    return db.query(models.User).filter(models.User.email == email).first()

# def create_user(db : Session, skip : int = 0, limit : int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    user = get_user_by_email(db, email)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+ expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, secretkey, algorithm)
    return encoded_jwt

def decode_access_token(token : str):
    decode_jwt = jwt.decode(token,secretkey, algorithm)
    return decode_jwt

def refresh_access_token(token : str):
    token_data = decode_access_token(token)
    to_encode = token_data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, secretkey, algorithm)
    return encoded_jwt

def get_category(db : Session):
    return db.query(models.Category).all()

def create_category(db : Session, item : schema.CategoryCreate):
    
    db_item = models.Category(title = item.title)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_product(db : Session, item : schema.ProductCreate):
    db_item = models.Product(
        name = item.name,
        price = float(item.price),
        category_id = item.category_id,
        description = item.description
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item