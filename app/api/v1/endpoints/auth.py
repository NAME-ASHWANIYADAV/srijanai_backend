from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import random
from datetime import datetime
import uuid
from google.oauth2 import id_token
from google.auth.transport import requests
from starlette.responses import RedirectResponse

from app.schemas.user import UserCreate, EmailVerify, UserLogin, Token, ForgotPassword, ResetPassword
from app.crud import password_reset as crud_password_reset
from app.services.email_service import send_otp_email, send_password_reset_email
from app.core.google_oauth import get_google_flow
from app.core.security import verify_password, create_access_token, get_password_hash
from app.crud import user as crud_user
from app.crud import otp as crud_otp
from app.db.mongodb import get_database
from app.core.config import settings

router = APIRouter()

@router.post("/reset-password")
async def reset_password(
    reset_password_in: ResetPassword,
    db: AsyncIOMotorClient = Depends(get_database)
):
    token_obj = await crud_password_reset.get_reset_token(db, token=reset_password_in.token)
    if not token_obj:
        raise HTTPException(
            status_code=400,
            detail="Invalid token.",
        )

    if token_obj["expires_at"] < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Token has expired.",
        )

    await crud_user.update_password(db, email=token_obj["email"], password=reset_password_in.password)
    await crud_password_reset.delete_reset_token(db, token=reset_password_in.token)

    return {"msg": "Password updated successfully."}

@router.post("/forgot-password")
async def forgot_password(
    forgot_password_in: ForgotPassword,
    db: AsyncIOMotorClient = Depends(get_database)
):
    user = await crud_user.get_user_by_email(db, email=forgot_password_in.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist.",
        )

    token = str(uuid.uuid4())
    await crud_password_reset.create_reset_token(db, email=forgot_password_in.email, token=token)
    await send_password_reset_email(email=forgot_password_in.email, token=token)

    return {"msg": "Password reset link sent to your email."}

@router.get("/google/login")
async def google_login():
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    return RedirectResponse(authorization_url)

@router.get("/google/callback")
async def google_callback(code: str, db: AsyncIOMotorClient = Depends(get_database)):
    flow = get_google_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token, 
        request=requests.Request(), 
        audience=settings.GOOGLE_CLIENT_ID
    )

    email = id_info.get("email")
    user = await crud_user.get_user_by_email(db, email=email)

    if not user:
        # Create a new user
        username = id_info.get("name")
        user_in = UserCreate(username=username, email=email, password=str(uuid.uuid4())) # Generate a random password
        user = await crud_user.create_user(db, user=user_in)
        await crud_user.activate_user(db, email=email)

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    user_in: UserLogin,
    db: AsyncIOMotorClient = Depends(get_database)
):
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive user. Please verify your email.",
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup(
    user_in: UserCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud_user.create_user(db, user=user_in)

    # Generate and send OTP
    otp = str(random.randint(100000, 999999))
    await crud_otp.create_otp(db, email=user_in.email, otp=otp)
    await send_otp_email(email=user_in.email, otp=otp)

    return {"msg": "User created successfully. Please check your email for OTP."}

@router.post("/verify-email")
async def verify_email(
    verify_in: EmailVerify,
    db: AsyncIOMotorClient = Depends(get_database)
):
    otp_obj = await crud_otp.get_otp(db, email=verify_in.email, otp=verify_in.otp)
    if not otp_obj:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP.",
        )
    
    if otp_obj["expires_at"] < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="OTP has expired.",
        )

    await crud_user.activate_user(db, email=verify_in.email)
    await crud_otp.delete_otp(db, email=verify_in.email, otp=verify_in.otp)

    return {"msg": "Email verified successfully."}