from create_api_app.config.settings import settings

from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    client: AsyncIOMotorClient = None


db = Database()


def get_db() -> AgnosticClient:
    """Retrieve the database client."""
    return db.client[settings.DB_NAME]
