from rest_framework import serializers
from .models import Conversation,Message
from lead.serializers import LeadSerializer
from sources.serializers import SourceSrializer
 

class ConversationSerializer(serializers.ModelSerializer):
    client_external_id = serializers.SerializerMethodField()
    source = SourceSrializer(source ="source_id",read_only = True)
    lead = LeadSerializer(source = "lead_id",read_only = True)

    class Meta:
        model = Conversation
        fields = ["id","client_external_id","current_state","last_message","source","lead"]

    def get_client_external_id(self, obj):
        return obj.lead_id.client_id.external_id
        


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