from django.shortcuts import render
from .models import Notifications
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .pagination import NotificationPagination

class NotificationAPiview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        notifications = Notifications.objects.all().order_by("-created_at")
        paginator = NotificationPagination()
        page = paginator.paginate_queryset(notifications,request)
        serializer = NotificationSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)
    
class NotificationMark(APIView):
    permission_classes = [IsAuthenticated]

    def get_obj(self,pk):
        try:
            return Notifications.objects.get(pk=pk)
        except Notifications.DoesNotExist:
            return None

    def post(self,request,pk):

        notification = self.get_obj(pk)

        if not notification:
            return Response({"error":"Notification not found"},status=status.HTTP_404_NOT_FOUND)
        

        is_read = request.data.get("is_read",True)
        
        notification.is_read = is_read
        notification.save()

        return Response(
            {
                "id":pk,
                "message": "Notification updated",
                "is_read": notification.is_read
            },
            status=status.HTTP_200_OK
        )
    

class NotificationSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
       
        settings = request.user.notifications_settings

        return Response({
            "new_lead": settings.new_lead,
            "booking": settings.booking,
            "sync_failures": settings.sync_failures,
            "weekly_reports": settings.weekly_reports,
            "auto_reminder": settings.auto_reminder,
        })

    def patch(self, request):
        
        settings = request.user.notifications_settings

        for key, value in request.data.items():
            setattr(settings, key, value)

        settings.save()
        return Response({"message": "Settings updated"})
        

