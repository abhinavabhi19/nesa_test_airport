from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.code


class AirportRoute(models.Model):
    POSITION_LEFT = 'L'
    POSITION_RIGHT = 'R'
    POSITION_CHOICES = [
        (POSITION_LEFT, 'Left'),
        (POSITION_RIGHT, 'Right'),
    ]

    source = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name='outgoing_routes')
    destination = models.ForeignKey(Airport,on_delete=models.CASCADE,related_name='incoming_routes'
    )
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)
    distance_km = models.PositiveIntegerField(help_text='Distance in kilometers')
    duration = models.PositiveIntegerField(help_text='Duration in minutes', null=True, blank=True)

    class Meta:
        unique_together = ('source', 'position')
        indexes = [
            models.Index(fields=['position']),
            models.Index(fields=['distance_km']),
        ]

    def __str__(self):
        return f"{self.source} → {self.destination} ({self.get_position_display()})"
