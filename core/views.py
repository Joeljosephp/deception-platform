from rest_framework import generics
from rest_framework.response import Response

from ai.risk_engine import analyze_security_events

from .models import SecurityEvent
from .serializers import SecurityEventSerializer


class SecurityEventListCreateView(generics.ListCreateAPIView):
    queryset = SecurityEvent.objects.all().order_by("-created_at")
    serializer_class = SecurityEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.save()

        ai_result = analyze_security_events([
            {
                "timestamp": event.timestamp.isoformat(),
                "user": event.user,
                "source_ip": event.source_ip,
                "action": event.action,
                "asset": event.asset,
                "event_type": event.event_type,
            }
        ])

        print("\n===== AI RESULT =====")
        print(ai_result)
        print("=====================\n")

        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "event": serializer.data,
                "ai_analysis": ai_result
            },
            status=201,
            headers=headers,
        )