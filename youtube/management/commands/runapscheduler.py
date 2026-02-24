from django.core.management.base import BaseCommand
from youtube.scheduler import start_scheduler
from youtube.bootstrap import bootstrap_jobs
import time

class Command(BaseCommand):
    help = "Run APScheduler"

    def handle(self, *args, **kwargs):
        bootstrap_jobs()
        start_scheduler()


        while True:
            time.sleep(60)
