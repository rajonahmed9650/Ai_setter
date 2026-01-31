from django.db import models

# Create your models here.

class Source(models.Model):
    PLATFORM_CHOICES = (
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("threads", "Threads"),
    )

    SOURCE_TYPE_CHOICES = (
        ("dm", "Direct Message"),
        ("post_comment", "Post Comment"),
    )
    platform = models.CharField(max_length=50,choices=PLATFORM_CHOICES,unique=True)
    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPE_CHOICES
    )
    app_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
