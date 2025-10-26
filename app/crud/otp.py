from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

async def create_otp(conn: AsyncIOMotorClient, email: str, otp: str):
    await conn.srijan_db.otps.insert_one({
        "email": email,
        "otp": otp,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    })

async def get_otp(conn: AsyncIOMotorClient, email: str, otp: str):
    return await conn.srijan_db.otps.find_one({"email": email, "otp": otp})

async def delete_otp(conn: AsyncIOMotorClient, email: str, otp: str):
    await conn.srijan_db.otps.delete_one({"email": email, "otp": otp})
