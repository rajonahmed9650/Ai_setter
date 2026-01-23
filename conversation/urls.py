from django.urls import path
from .views import ConversationApiview

urlpatterns = [
    path("conversation",ConversationApiview.as_view(),name="conversation"),
]
