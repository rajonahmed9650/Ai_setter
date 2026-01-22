from .models import Question,LeadScoringRule
from rest_framework import serializers

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class LeadScroingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadScoringRule
        fields = "__all__"

