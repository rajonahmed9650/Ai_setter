from django.conf import settings
from youtube.services.youtube_auth import get_youtube_client

def fetch_latest_comments():
    print("CHANNEL ID:", settings.YOUTUBE_CHANNEL_ID)

    youtube = get_youtube_client()

    res = youtube.commentThreads().list(
        part="snippet",
        allThreadsRelatedToChannelId=settings.YOUTUBE_CHANNEL_ID,
        order="time",
        maxResults=20
    ).execute()

    comments = []

    for item in res.get("items", []):
        top = item["snippet"]["topLevelComment"]["snippet"]

        comments.append({
            "comment_id": item["snippet"]["topLevelComment"]["id"],
            "text": top["textDisplay"],
            "author_name": top.get("authorDisplayName"),
            "author_channel_id": top.get("authorChannelId", {}).get("value"),
            "channel_id": settings.YOUTUBE_CHANNEL_ID,
        })

    return comments
