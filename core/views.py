from ai.risk_engine import analyze_security_events
from rest_framework import generics
from .models import SecurityEvent
from .serializers import SecurityEventSerializer


class SecurityEventListCreateView(generics.ListCreateAPIView):
    queryset = SecurityEvent.objects.all().order_by("-created_at")
    serializer_class = SecurityEventSerializer