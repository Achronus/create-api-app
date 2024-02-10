from contextlib import asynccontextmanager

from .db import db
from .db.models import ItemModel
from .config.settings import settings
from .routers import items, users

from beanie import init_beanie
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Open DB connection
    db.client = AsyncIOMotorClient(
        settings.DB_URL, 
        server_api=ServerApi('1')
    )
    await init_beanie(
        database=db.client[settings.DB_NAME],
        document_models=[ItemModel]
    )

    # Perform routes...
    yield

    # Close DB connection
    db.client.close()


# Define FastAPI app its mounts and routers
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=settings.DIRPATHS.PUBLIC), name="static")

app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def home(request: Request):
    return {"name": "Hello world!"}
