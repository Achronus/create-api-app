from typing import Optional

from app.config.settings import settings

from beanie import Document
from pydantic import BaseModel


class ExampleDB(Document):
    """
    The main model for your database collection. Should represent the structure of the data in the collection.

    For more details check the [Beanie docs](https://beanie-odm.dev/).
    """

    name: str
    desc: Optional[str] = None

    class Settings:
        name = settings.DB_COLLECTION_NAME


__beanie_models__ = [ExampleDB]
