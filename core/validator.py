import re

from fastapi import HTTPException

REGEX_USERNAME = '^[a-z0-9+]{3,15}$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,15}$'
REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def validate_username(username):
    if not re.match(REGEX_USERNAME, username):
        raise HTTPException(
            status_code=401,
            detail="Invalid username")
    return username

def validate_password(password):
    if not re.match(REGEX_PASSWORD, password):
        raise HTTPException(status_code=401,detail="Invalid password")
    return password

def validate_email(email):
    if not re.match(REGEX_EMAIL, email):
        raise HTTPException(status_code=401,detail="Invalid email")
    return email