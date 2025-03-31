"""Main FastAPI app"""

from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from .services.database import init_db, get_session
from .models import Shoe


async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/get-db/")
async def get_db():
    return {"Hello  World?"}
