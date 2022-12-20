from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.databases import Base, engine
from database import models
from routes import users,products
import sys, os
from core.log import LOG, setup as log_setup
from pathlib import Path
import logging.handlers
from datetime import date
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

log_setup(Path("./log/").joinpath(f"{str(date.today())}.log"))
# Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
async def root():
    Base.metadata.create_all(bind=engine)
    LOG.success("Welcome Back")
    return {"message" : "Hello JeongHyeon Wellcome Back"}