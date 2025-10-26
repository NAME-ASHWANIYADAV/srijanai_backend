from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import UserInDB
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def create_user(conn: AsyncIOMotorClient, user: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(**user.dict(exclude={"password"}), hashed_password=hashed_password)
    await conn.srijan_db.users.insert_one(db_user.dict())
    return db_user

async def get_user_by_email(conn: AsyncIOMotorClient, email: str) -> UserInDB:
    user = await conn.srijan_db.users.find_one({"email": email})
    if user:
        return UserInDB(**user)

async def activate_user(conn: AsyncIOMotorClient, email: str) -> None:
    await conn.srijan_db.users.update_one({"email": email}, {"$set": {"is_active": True}})

async def update_password(conn: AsyncIOMotorClient, email: str, password: str) -> None:
    hashed_password = get_password_hash(password)
    await conn.srijan_db.users.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})
