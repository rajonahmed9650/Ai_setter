from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ConversationSerializer
from .models import Conversation
# Create your views here.

class ConversationApiview(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        conversation = Conversation.objects.all()
        serializers = ConversationSerializer(conversation,many=True)
        return Response(serializers.data)


