from .models import Question,LeadScoringRule,Lead
from rest_framework import serializers
from clients.serializers import ClientSerializers

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class LeadScroingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadScoringRule
        fields = "__all__"


class LeadSerializer(serializers.ModelSerializer):
    # client = ClientSerializers(source = "client_id", read_only = True)
    class Meta:
        model = Lead
        fields = ["id","client_id","score","status","last_response",]
