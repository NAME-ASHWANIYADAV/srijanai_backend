from pydantic import BaseModel, EmailStr, constr
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: constr(max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmailVerify(BaseModel):
    email: EmailStr
    otp: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    password: str

class UserInDBBase(UserBase):
    id: uuid.UUID
    username: str
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
