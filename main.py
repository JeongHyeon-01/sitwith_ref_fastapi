from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.databases import Base, engine
from database import models
from routes import users,products
import sys
sys.setrecursionlimit(9999)
app = FastAPI()
'''
CORS 
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"]
)


# Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
async def root():
    Base.metadata.create_all(bind=engine)
    return {"message" : "Hello JeongHyeon Wellcome Back"}