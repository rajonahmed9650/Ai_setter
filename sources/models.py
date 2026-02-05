from django.db import models
from django.conf import settings
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sources",
        null=True,
        blank=True
    )

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES
    )
    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPE_CHOICES
    )
    app_id = models.CharField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("platform", "source_type")

    
