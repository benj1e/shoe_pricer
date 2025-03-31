"""Main FastAPI app"""

from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from .database import init_db, get_session
from .crud import add_shoe
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


@app.post("/add-shoe/")
async def _add_shoe(shoe: Shoe):
    session = get_session()
    shoe = add_shoe(shoe, session)
    return {"shoe": shoe}
