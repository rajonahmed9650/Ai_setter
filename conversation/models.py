from django.db import models
from lead.models import Lead
from sources.models import Source
# Create your models here.
class Conversation(models.Model):
    lead_id =  models.ForeignKey(Lead,on_delete=models.CASCADE)
    source_id = models.ForeignKey(Source,on_delete=models.CASCADE)
    current_state = models.CharField(max_length=50, null=True, blank=True)
    user_attributes = models.JSONField(default=dict)
    last_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    SENDER_TYPE = (
        ("bot","BOt"),
        ("client","Client")
    )
    conversation_id = models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name="messages")
    sender_type = models.CharField(max_length=20,choices=SENDER_TYPE)
    message = models.JSONField()
    platform = models.CharField(max_length=50, null=True, blank=True)

    external_comment_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

