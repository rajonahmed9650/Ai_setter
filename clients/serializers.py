from rest_framework import serializers
from .models import Client

class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id","external_id","name","email","phone"]