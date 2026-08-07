from rest_framework import serializers
from .models import SecurityEvent


class SecurityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityEvent
        fields = [
            "id",
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