from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database.databases import get_db
from database.schema import ResponseUser, RequestUser
from typing import List
from database.models import User
from database.databases import Base, engine
app = FastAPI()
'''
CORS 
'''
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"]
)


Base.metadata.create_all(bind=engine)

@app.get("/")
async def  making():
    return {"hello":"hi"}

@app.get("/test", response_model=List[ResponseUser])
async def get_tests(db: Session = Depends(get_db)):
    memos = db.query(User).all()
    return memos

@app.post("/tests")
async def register_test(
    req : RequestUser,
    db : Session = Depends(get_db)
    ):
    
    test = User(**req.dict())
    
    db.add(test)
    
    db.commit()
    return User