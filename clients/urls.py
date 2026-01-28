from django.urls import path
from .views import MessageView
from .webhooks.views import FacebookWebhookView

urlpatterns = [
    path("message/",MessageView.as_view(),name="message"),
    path("webhooks/facebook/",FacebookWebhookView.as_view(),name="webhooks"),
]
