from django.db import models
from clients.models import Client
from accounts.models import User
# Create your models here.


class Notifications(models.Model):
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notifications_settings(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    new_lead = models.BooleanField(default=True)
    booking = models.BooleanField(default=True)
    sync_failures = models.BooleanField(default=True)
    weekly_reports = models.BooleanField(default=True)
    auto_reminder = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

