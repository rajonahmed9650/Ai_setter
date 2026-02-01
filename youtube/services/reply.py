from .youtube_auth import get_youtube_client
def send_youtube_comment_reply(parent_comment_id, text):
    youtube = get_youtube_client()

    youtube.comments().insert(
        part="snippet",
        body={
            "snippet": {
                "parentId": parent_comment_id,
                "textOriginal": text
            }
        }
    ).execute()

    print("✅ YouTube reply sent")

