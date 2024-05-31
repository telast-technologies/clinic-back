from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models

from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin
from clinic.utils.validators import RangeValidator
from clinic.visits.choices import DaysOfWeek, VisitStatus, VisitType


class TimeSlot(models.Model):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="time_slots", editable=False
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = ArrayField(models.CharField(max_length=10, choices=DaysOfWeek.choices), size=7)

    def clean(self):
        super().clean()
        RangeValidator(self.start_time, self.end_time)()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Days: [{', '.join(self.days)}] | {self.start_time} - {self.end_time}"


class Visit(UUIDAutoFieldMixin, TimestampMixin):
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

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("patient", "date")


class ChargeService(UUIDAutoFieldMixin, TimestampMixin):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="charge_services")
    service = models.ForeignKey("healthcare.Service", on_delete=models.CASCADE, related_name="charge_services")

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("visit", "service")

    @property
    def charge(self):
        return self.service.charge


class ChargeItem(UUIDAutoFieldMixin, TimestampMixin):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="charge_items")
    supply = models.ForeignKey("inventory.Supply", on_delete=models.CASCADE, related_name="charge_items")
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("visit", "supply")

    @property
    def charge(self):
        return self.quantity * self.supply.unit_sales_price
