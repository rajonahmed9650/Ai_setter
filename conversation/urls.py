from django.urls import path
from .views import ConversationApiview,ConversationMessageApiView,DashboardApiView

urlpatterns = [
    path("conversation",ConversationApiview.as_view(),name="conversation"),
    path("conversation/<int:conversation_id>",ConversationMessageApiView.as_view(),name="conversation"),
    path("dashboard",DashboardApiView.as_view(),name="dashboard")
]
