from rest_framework import serializers
from .models import Conversation
from lead.serializers import LeadSerializer
from sources.serializers import SourceSrializer


class ConversationSerializer(serializers.ModelSerializer):
    source = SourceSrializer(source ="source_id",read_only = True)
    lead = LeadSerializer(source = "lead_id",read_only = True)

    class Meta:
        model = Conversation
        fields = ["id","current_state","last_message","source","lead"]
    