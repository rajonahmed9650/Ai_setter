from .models import Source
from rest_framework import serializers


class SourceSrializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ["id","platform","app_id"]


