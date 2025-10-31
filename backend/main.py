from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import tracker_api
from db import base, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(tracker_api)
base.metadata.create_all(bind=engine)
