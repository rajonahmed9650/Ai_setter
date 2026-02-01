import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_youtube_client():
    creds = None

    if settings.YOUTUBE_TOKEN_PATH.exists():
        with open(settings.YOUTUBE_TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.YOUTUBE_CLIENT_SECRET_PATH,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(settings.YOUTUBE_TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)
