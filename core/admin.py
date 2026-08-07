from django.contrib import admin
from .models import SecurityEvent


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "user",
        "source_ip",
        "action",
        "asset",
        "event_type",
        "severity",
    )

    list_filter = (
        "event_type",
        "severity",
    )

    search_fields = (
        "user",
        "source_ip",
        "asset",
        "incident_id",
    )