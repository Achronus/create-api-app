from ..db.models import ItemModel

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from motor.core import AgnosticClient


async def add(client: AgnosticClient, name: str, document: ItemModel) -> str:
    """Inserts a document into the given collection name."""
    try:
        result = await client[name].insert_one(document.model_dump())
        return str(result.inserted_id)
    except DuplicateKeyError:
        print("An item with this name already exists.")


async def get(client: AgnosticClient, name: str, id: str) -> dict:
    return await client[name].find_one({"_id": ObjectId(id)})


async def update(client: AgnosticClient, name: str, id: str, update_values: dict) -> dict:
    try:
        await client[name].update_one({"_id": ObjectId(id)}, {"$set": update_values})
        return get(name, id)
    except DuplicateKeyError:
        print("An item with this name already exists.")


async def delete(client: AgnosticClient, name: str, id: str) -> dict:
    await client[name].delete_one({"_id": ObjectId(id)})
    return {"status": "Item deleted."}


async def get_multiple(client: AgnosticClient, name: str, limit: int = 10) -> list[dict]:
    cursor = client[name].find().limit(limit)
    return await cursor.to_list(length=limit)
