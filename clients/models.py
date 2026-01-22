from django.db import models
from sources.models import Source

# Create your models here.
class Client(models.Model):
    external_id = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone =models.CharField()
    location = models.CharField(max_length=50)
    source_id = models.ForeignKey(Source,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("external_id", "source_id")

class Tag(models.Model):
    tags_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tagged_lead(models.Model):
    tag_id = models.ForeignKey(Tag,on_delete=models.CASCADE)
    client_id = models.ForeignKey(Client,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    