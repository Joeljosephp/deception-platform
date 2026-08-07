from django.db import models

# Create your models here.


class SecurityEvent(models.Model):
    timestamp = models.DateTimeField()
    user = models.CharField(max_length=150)
    source_ip = models.GenericIPAddressField()
    action = models.CharField(max_length=100)
    asset = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100)

    severity = models.CharField(max_length=50, blank=True)
    incident_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.user} - {self.source_ip}"