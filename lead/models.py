from django.db import models
from clients.models import Client
# Create your models here.
class Lead(models.Model):
    CHOICES = (
        ("hot lead","Hot Lead"),
        ("warm lead","Warm Lead"),
        ("nature","Nature")
    )
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=50,choices=CHOICES)
    notification_sent = models.BooleanField(default=False)
    last_response = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeadScoringRule(models.Model):
    title = models.CharField(max_length=255)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
 

class Question(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question       