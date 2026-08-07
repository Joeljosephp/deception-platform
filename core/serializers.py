from rest_framework import serializers

from .models import SecurityEvent, Attacker


class SecurityEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecurityEvent

        fields = [
            "id",
            "attacker",
            "timestamp",
            "user",
            "source_ip",
            "action",
            "asset",
            "event_type",
            "severity",
            "incident_id",
            "created_at",
        ]


class AttackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attacker

        fields = [
            "id",
            "name",
            "source_ip",
            "status",
            "created_at",
        ]