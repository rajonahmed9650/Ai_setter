from django.db import models
from lead.models import Lead
from clients.models import Client
# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = (
        ("completed","Completed"),
        ("cancelled","Cancelled")
    )

    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    meeting_link = models.CharField(max_length=255)
    note = models.TextField(blank=True , null= True)
    status = models.CharField(max_length=40,choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return super().__str__()
    