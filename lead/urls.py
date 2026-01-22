from django.urls import path
from .views import QuestionListApiView,QuestionDetailsApiView,LeadScoringApiView,LeadScoringDetailsView

urlpatterns = [
    path("question",QuestionListApiView.as_view(),name="question"),
    path("question/<int:pk>",QuestionDetailsApiView.as_view(),name="single_question"),
    path("leadscore",LeadScoringApiView.as_view(),name="leadscore"),
    path("leadscore/<int:pk>",LeadScoringDetailsView.as_view(),name="single_leadscore"),
]
