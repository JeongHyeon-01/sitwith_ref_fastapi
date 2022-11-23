from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def  making():
    return {"hello":"hi"}
