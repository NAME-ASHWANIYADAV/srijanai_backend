from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

async def create_reset_token(conn: AsyncIOMotorClient, email: str, token: str):
    await conn.srijan_db.password_reset_tokens.insert_one({
        "email": email,
        "token": token,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    })

async def get_reset_token(conn: AsyncIOMotorClient, token: str):
    return await conn.srijan_db.password_reset_tokens.find_one({"token": token})

async def delete_reset_token(conn: AsyncIOMotorClient, token: str):
    await conn.srijan_db.password_reset_tokens.delete_one({"token": token})
