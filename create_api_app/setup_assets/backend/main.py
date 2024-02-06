from .config.settings import settings
from .routers import items, users

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.DIRPATHS.PUBLIC), name="static")

app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def home(request: Request):
    return {"name": "Hello world!"}
