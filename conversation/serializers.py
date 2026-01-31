from rest_framework import serializers
from .models import Conversation,Message
from lead.serializers import LeadSerializer
from sources.serializers import SourceSrializer
 

class ConversationSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField()
    client_external_id = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    source = SourceSrializer(source ="source_id",read_only = True)
    lead = LeadSerializer(source = "lead_id",read_only = True)

    class Meta:
        model = Conversation
        fields = ["id","client_id","client_external_id","client_name","current_state","last_message","source","lead"]

    def get_client_id(self, obj):
        return obj.lead_id.client_id.id


    def get_client_external_id(self, obj):
        return obj.lead_id.client_id.external_id
    
    def get_client_name(self, obj):
        return obj.lead_id.client_id.name
        


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = [
            "id",
            "sender_type",
            "message",
            "created_at",
            "updated_at",
        ]