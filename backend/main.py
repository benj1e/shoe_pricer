"""Main FastAPI app"""

from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from .services.database import init_db, get_session
# from .models import Shoe
from .routers import shoes, stores, price_alerts, price_history


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(shoes.router)
app.include_router(stores.router)
app.include_router(price_history.router)


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/get-db/")
async def get_db():
    return {"Hello  World?"}
