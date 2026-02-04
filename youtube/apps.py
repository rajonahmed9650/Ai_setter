import os
from django.apps import AppConfig

class YoutubeConfig(AppConfig):
    name = "youtube"

    def ready(self):
        if os.environ.get("RUN_MAIN") != "true":
            return

        from youtube.scheduler import start_scheduler
        from youtube.bootstrap import bootstrap_jobs

        bootstrap_jobs()
        start_scheduler()
