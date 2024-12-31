from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_extensions.db.fields import RandomCharField

from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin
from clinic.visits.choices import DaysOfWeek, VisitStatus, VisitType


class TimeSlot(models.Model):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="time_slots", editable=False
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = ArrayField(models.CharField(max_length=10, choices=DaysOfWeek.choices), size=7)

    def __str__(self):
        return f"Days: [{', '.join(self.days)}] | {self.start_time} - {self.end_time}"


class Visit(UUIDAutoFieldMixin, TimestampMixin):
    no = RandomCharField(
        length=6,
        help_text="Visit number",
        unique=True,
        include_alpha=False,
        include_punctuation=False,
        include_digits=True,
    )
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="visits")
    date = models.DateField()
    time = models.TimeField()
    visit_type = models.CharField(
        max_length=20,
        choices=VisitType.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=VisitStatus.choices,
        default=VisitStatus.BOOKED,
    )
    comment = models.TextField(default="", blank=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("patient", "date")
