from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_otp_email(email: str, otp: str):
    html = f"""
    <p>Hi,</p>
    <p>Thanks for signing up for SrijanAI. Your OTP for email verification is <strong>{otp}</strong>.</p>
    <p>This OTP is valid for 10 minutes.</p>
    <p>Thanks,</p>
    <p>The SrijanAI Team</p>
    """

    message = MessageSchema(
        subject="SrijanAI Email Verification",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

async def send_password_reset_email(email: str, token: str):
    reset_link = f"https://srijanai.vercel.app/reset-password?token={token}"
    html = f"""
    <p>Hi,</p>
    <p>You have requested to reset your password. Click the link below to reset your password:</p>
    <p><a href="{reset_link}">{reset_link}</a></p>
    <p>This link is valid for 10 minutes.</p>
    <p>Thanks,</p>
    <p>The SrijanAI Team</p>
    """

    message = MessageSchema(
        subject="SrijanAI Password Reset",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
