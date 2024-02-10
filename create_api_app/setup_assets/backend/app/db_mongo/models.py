from typing import Optional

from pydantic import BaseModel, Field
from beanie import Document, Indexed


class ItemModel(Document):
    """Container for a single Item."""
    name: str = Indexed(str, unique=True)
    description: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Demo item",
                "description": "This is a demo item. Use it wisely!",
            }
        }


class UpdateItemModel(BaseModel):
    """A container for updating a Item in the database."""
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Demo item",
                "description": "This is a demo item. Use it wisely!",
            }
        }


class ItemCollection(BaseModel):
    """A container holding a list of `ItemModel` instances."""
    items: list[ItemModel]


def ResponseModel(data: list[dict], message: str) -> dict:
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error: str, code: int, message: str) -> dict:
    return {
        "error": error,
        "code": code,
        "message": message
    }
