from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.risk_engine import analyze_security_events

from .models import SecurityEvent, Attacker
from .serializers import (
    SecurityEventSerializer,
    AttackerSerializer,
)


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


class AIAnalysisView(APIView):

    def get(self, request):

        events = (
            SecurityEvent.objects
            .all()
            .order_by("-created_at")[:10]
        )

        event_list = []

        for event in events:

            event_list.append({
                "timestamp": event.timestamp.isoformat(),
                "user": event.user,
                "source_ip": event.source_ip,
                "action": event.action,
                "asset": event.asset,
                "event_type": event.event_type,
            })

        result = analyze_security_events(event_list)

        return Response(result)


class DashboardStatsView(APIView):

    def get(self, request):

        total_events = SecurityEvent.objects.count()

        alerts = SecurityEvent.objects.filter(
            Q(severity__iexact="Critical") |
            Q(severity__iexact="High")
        ).count()

        incidents = (
            SecurityEvent.objects
            .exclude(incident_id="")
            .values("incident_id")
            .distinct()
            .count()
        )

        return Response({
            "active_decoys": 10,
            "threats": total_events,
            "alerts": alerts,
            "incidents": incidents
        })
class AttackerListView(APIView):

    def get(self, request):

        attackers = Attacker.objects.all().order_by("id")

        serializer = AttackerSerializer(
            attackers,
            many=True
        )

        return Response(serializer.data)


class AttackerSimulationView(APIView):

    def post(self, request, attacker_id):

        try:
            attacker = Attacker.objects.get(id=attacker_id)

        except Attacker.DoesNotExist:

            return Response(
                {
                    "error": "Attacker not found"
                },
                status=404
            )

        attack_type = request.data.get(
            "attack_type",
            "honeytoken"
        )

        # ==========================================
        # HONEYTOKEN ATTACK
        # ==========================================

        if attack_type == "honeytoken":

            event_data = {
                "attacker": attacker.id,
                "timestamp": request.data.get("timestamp"),
                "user": attacker.name,
                "source_ip": attacker.source_ip,
                "action": "access",
                "asset": "fake_api_key",
                "event_type": "honeytoken_access",
                "severity": "Critical",
                "incident_id": request.data.get(
                    "incident_id",
                    ""
                )
            }

        # ==========================================
        # FAKE DOCUMENT ATTACK
        # ==========================================

        elif attack_type == "document":

            event_data = {
                "attacker": attacker.id,
                "timestamp": request.data.get("timestamp"),
                "user": attacker.name,
                "source_ip": attacker.source_ip,
                "action": "open",
                "asset": "salary.xlsx",
                "event_type": "fake_document",
                "severity": "High",
                "incident_id": request.data.get(
                    "incident_id",
                    ""
                )
            }

        # ==========================================
        # ADMIN API SCAN
        # ==========================================

        elif attack_type == "scan":

            event_data = {
                "attacker": attacker.id,
                "timestamp": request.data.get("timestamp"),
                "user": attacker.name,
                "source_ip": attacker.source_ip,
                "action": "scan",
                "asset": "admin_api",
                "event_type": "network_scan",
                "severity": "High",
                "incident_id": request.data.get(
                    "incident_id",
                    ""
                )
            }

        # ==========================================
        # UNKNOWN ATTACK
        # ==========================================

        else:

            return Response(
                {
                    "error": "Unknown attack type",
                    "available_attacks": [
                        "honeytoken",
                        "document",
                        "scan"
                    ]
                },
                status=400
            )

        # ==========================================
        # CREATE SECURITY EVENT
        # ==========================================

        serializer = SecurityEventSerializer(
            data=event_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        event = serializer.save()

        # ==========================================
        # RUN AI / RISK ANALYSIS
        # ==========================================

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

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return Response(
            {
                "attacker": {
                    "id": attacker.id,
                    "name": attacker.name,
                    "source_ip": attacker.source_ip
                },

                "event": serializer.data,

                "ai_analysis": ai_result
            },
            status=201
        )