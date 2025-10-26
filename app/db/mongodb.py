from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class DataBase:
    client: AsyncIOMotorClient = None

db = DataBase()

async def get_database() -> AsyncIOMotorClient:
    return db.client

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard")

async def close_mongo_connection():
    db.client.close()
