from django.db import models

# Create your models here.

class Source(models.Model):
    PLATFORM_CHOICES = (
        ("instagram","Instagram"),
        ("facebook","Facebook"),
        ("linkedin","LinkedIn"),
    )
    platform = models.CharField(max_length=50,choices=PLATFORM_CHOICES)
    app_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    