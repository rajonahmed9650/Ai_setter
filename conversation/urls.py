from django.urls import path
from .views import ConversationApiview,ConversationMessageApiView

urlpatterns = [
    path("conversation",ConversationApiview.as_view(),name="conversation"),
    path("conversation/<int:conversation_id>",ConversationMessageApiView.as_view(),name="conversation"),
]
