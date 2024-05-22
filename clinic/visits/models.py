from django.contrib.postgres.fields import ArrayField
from django.db import models

from clinic.visits.choices import DaysOfWeek


class TimeSlot(models.Model):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="time_slots", editable=False
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = ArrayField(models.CharField(max_length=10, choices=DaysOfWeek.choices), size=7)

    def __str__(self):
        return f"Days: [{', '.join(self.days)}] | {self.start_time} - {self.end_time}"
