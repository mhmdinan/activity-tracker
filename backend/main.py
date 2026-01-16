from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import api
from db import base, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api, prefix="/api")
base.metadata.create_all(bind=engine)
