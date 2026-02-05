from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ConversationSerializer,MessageSerializer
from .models import Conversation,Message
from notifications.pagination import NotificationPagination
from lead.models import Lead
from django.utils import timezone
from datetime import timedelta
# Create your views here.

class ConversationApiview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        conversation = Conversation.objects.all().order_by("-created_at")

        paginator = NotificationPagination()

        page = paginator.paginate_queryset(conversation,request)

        serializers = ConversationSerializer(page,many=True)
        return paginator.get_paginated_response(serializers.data)


class ConversationMessageApiView(APIView):
    permission_classes = [IsAuthenticated]

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
    



class DashboardApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 🔹 Total messages (client + bot)
        total_message = Message.objects.count()

        # 🔹 Identified leads (warm + hot)
        total_leads = Lead.objects.filter(
            status__in=["warm lead", "hot lead"]
        ).count()

        today = timezone.now().date()
        data = []

        # 🔹 Day-wise ALL messages (bot + client)
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)

            count = Message.objects.filter(
                created_at__date=day
            ).count()

            data.append({
                "day": day.strftime("%a"),
                "count": count
            })

        return Response({
            "total_message": total_message,
            "total_leads": total_leads,
            "data": data
        })   
