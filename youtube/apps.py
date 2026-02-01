# youtube/apps.py
import os
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

class YoutubeConfig(AppConfig):
    name = "youtube"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return

        #  IMPORT INSIDE ready()
        from youtube.jobs import youtube_comment_job

        scheduler = BackgroundScheduler()
        scheduler.add_job(
            youtube_comment_job,
            "interval",
            minutes=5,
            max_instances=1,
            coalesce=True,
            id="youtube_comment_job"
        )

        scheduler.start()
