from google_auth_oauthlib.flow import Flow
from app.core.config import settings

def get_google_flow():
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
        }
    }
    return Flow.from_client_config(
        client_config=client_config,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
