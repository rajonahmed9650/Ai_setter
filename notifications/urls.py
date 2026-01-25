from django.urls import path
from .views import NotificationAPiview,NotificationMark,NotificationSettingsView



urlpatterns = [
    path("notifications",NotificationAPiview.as_view(),name="notifications"),
    path("notifications/mark/<int:pk>",NotificationMark.as_view(),name="notifications"),
    path("settings/", NotificationSettingsView.as_view()),
]
