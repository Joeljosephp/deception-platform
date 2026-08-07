from django.urls import path
from .views import SecurityEventListCreateView


urlpatterns = [
    path("events/", SecurityEventListCreateView.as_view(), name="events"),
]