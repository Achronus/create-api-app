# Changing From MongoDB to SQL

!!! note
    This section focuses on updates to the [`backend`](#changing-from-mongodb-to-sql) directory. Remember to [`cd`](#changing-from-mongodb-to-sql) into it first!

This tool doesn't currently support [`SQL`](#changing-from-mongodb-to-sql) databases and likely won't do in the future.

However, it is still possible to use [`SQL`](#changing-from-mongodb-to-sql) with the tool, you just need to configure this yourself. We recommend checking out FastAPI's great [documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/) on how to do this.

## Cleaning Up MongoDB Files

If you choose this option, you'll need to remove the [`beanie`](#cleaning-up-mongodb-files) package from the `backend`. You can do this by running the poetry remove command while inside the `backend` directory:

```python title=""
poetry remove beanie
```

Additionally, you need to update a couple of files inside the [`app`](#cleaning-up-mongodb-files) directory:

- `db/__init__.py`
- `main.py` - the lifespan method

### DB Init File

Remove `all` the lines in the file but keep the file there so you can still use the [`db`](#db-init-file) directory.

??? tip "Why keep the __init__ file?"
    `__init__.py` files tell Python that a folder should be treated as a package so that you can import and use its modules in your code.

    Starting with `Python 3.3`, it is not strictly required, but it is still useful for other purposes. You can read more about this in the [Python documentation](https://docs.python.org/3/tutorial/modules.html).

```python title="db/__init__.py" hl_lines="1-12"
from app.models import __beanie_models__
from app.config.settings import settings

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


async def init_db() -> None:
    """Initialises the database."""
    client = AsyncIOMotorClient(settings.DB_URL)
    database = client[settings.DB_NAME]
    await init_beanie(database=database, document_models=__beanie_models__)
```

## The Main File

Remove lines `1-3` and `9-12` and update line `15`.

```python title="main.py" hl_lines="1-3 9-12 15"
from contextlib import asynccontextmanager

from app.db import init_db

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(docs_url="/api/docs", redoc_url=None, lifespan=lifespan) # (1)!

# app.include_router(root.router, prefix="/api")

origins = [
    "",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

1. Remove [`lifespan=lifespan`](#the-main-file)
