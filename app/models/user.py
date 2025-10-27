from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid

class User(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = False
    is_superuser: bool = False
    google_id: Optional[str] = None

class UserInDB(User):
    class Config:
        from_attributes = True
