from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import ConversationSerializer,MessageSerializer
from .models import Conversation,Message
from notifications.pagination import NotificationPagination
# Create your views here.

class ConversationApiview(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        conversation = Conversation.objects.all().order_by("-created_at")

        paginator = NotificationPagination()

        page = paginator.paginate_queryset(conversation,request)

        serializers = ConversationSerializer(page,many=True)
        return paginator.get_paginated_response(serializers.data)


class ConversationMessageApiView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,conversation_id):
        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation:
            return Response({"error":"Conversation not found"},status=status.HTTP_404_NOT_FOUND)
        messages = Message.objects.filter(conversation_id = conversation_id)

        if not messages:
            return Response({"error":"Messages not found"},status=status.HTTP_404_NOT_FOUND)
        
        conversation_serializer = ConversationSerializer(conversation)
        
        serializer = MessageSerializer(messages,many = True)
        return Response({
            "coversation":conversation_serializer.data,
            "messages": serializer.data
        })
    
