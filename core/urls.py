from django.urls import path
from .views import SecurityEventListCreateView, AIAnalysisView

urlpatterns = [
    path("events/", SecurityEventListCreateView.as_view(), name="events"),
    path("analysis/", AIAnalysisView.as_view(), name="analysis"),
]