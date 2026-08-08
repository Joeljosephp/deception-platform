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
from django.shortcuts import render
from ai.ai_analyst import chat_with_ai

def login_view(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "index.html")


def threats(request):
    return render(request, "threats.html")


def attackers(request):
    return render(request, "attackers.html")
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


class AIChatView(APIView):
    def post(self, request):
        question = request.data.get("question", "")
        
        # Get recent events to give context
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
            
        from ai.incident_report import generate_report
        # Quick fake risk/threat to just dump the event log as context
        report = generate_report(100, "CRITICAL", [str(e) for e in event_list])
        
        prompt = f"System Context: You are an elite SOC AI assistant.\n\nRecent Incident Context:\n{report}\n\nUser Question: {question}"
        
        result = chat_with_ai(prompt)
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
        
        from django.utils import timezone
        import datetime
        now = timezone.now()
        chart_data = []
        for i in range(24, -1, -1):
            start_time = now - datetime.timedelta(hours=i)
            end_time = now - datetime.timedelta(hours=i-1)
            count = SecurityEvent.objects.filter(timestamp__gte=start_time, timestamp__lt=end_time).count()
            chart_data.append({
                "time": start_time.strftime("%H:00"),
                "count": count
            })

        return Response({
            "active_decoys": 5,
            "threats": total_events,
            "alerts": alerts,
            "incidents": incidents,
            "chart_data": chart_data
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
        # FAKE DATABASE ATTACK
        # ==========================================

        elif attack_type == "cc_data":

            event_data = {
                "attacker": attacker.id,
                "timestamp": request.data.get("timestamp"),
                "user": attacker.name,
                "source_ip": attacker.source_ip,
                "action": "download",
                "asset": "customer_cc_data.db",
                "event_type": "fake_database",
                "severity": "Critical",
                "incident_id": request.data.get(
                    "incident_id",
                    ""
                )
            }

        # ==========================================
        # FAKE PASSWORDS FILE ATTACK
        # ==========================================

        elif attack_type == "passwords":

            event_data = {
                "attacker": attacker.id,
                "timestamp": request.data.get("timestamp"),
                "user": attacker.name,
                "source_ip": attacker.source_ip,
                "action": "open",
                "asset": "passwords.txt",
                "event_type": "fake_passwords",
                "severity": "Critical",
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
                        "scan",
                        "cc_data",
                        "passwords"
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

class ResetDatabaseView(APIView):
    def post(self, request):
        try:
            # Delete all events
            SecurityEvent.objects.all().delete()
            # Reset all attacker statuses
            Attacker.objects.all().update(status="Active")
            return Response({"message": "Database reset successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)