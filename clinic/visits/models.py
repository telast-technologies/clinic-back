from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from django_fsm import FSMField, transition

from clinic.utils.models import TimestampMixin, UUIDMixin
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


class Visit(UUIDMixin, TimestampMixin):
    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="visits")
    date = models.DateField()
    time = models.TimeField()
    visit_type = models.CharField(
        max_length=20,
        choices=VisitType.choices,
    )
    status = FSMField(
        max_length=20,
        choices=VisitStatus.choices,
        default=VisitStatus.BOOKED,
        protected=True,
    )

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("patient", "date")

    @transition(field=status, source=[VisitStatus.BOOKED], target=VisitStatus.CHECKED_IN)
    def check_in(self):
        pass

    @transition(field=status, source=[VisitStatus.CHECKED_IN], target=VisitStatus.FINANCIALLY_CLEARED)
    def financially_clear(self):
        pass

    @transition(field=status, source=[VisitStatus.FINANCIALLY_CLEARED], target=VisitStatus.CHECKED_OUT)
    def check_out(self):
        pass

    @transition(field=status, source=[VisitStatus.BOOKED, VisitStatus.CHECKED_IN], target=VisitStatus.CANCELLED)
    def cancel(self, reason):
        pass


class ChargeService(UUIDMixin, TimestampMixin):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="charge_services")
    service = models.ForeignKey("healthcare.Service", on_delete=models.CASCADE, related_name="charge_services")

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("visit", "service")

    @property
    def charge(self):
        return self.service.charge


class ChargeItem(UUIDMixin, TimestampMixin):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="charge_items")
    supply = models.ForeignKey("inventory.Supply", on_delete=models.CASCADE, related_name="charge_items")
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("visit", "supply")

    @property
    def charge(self):
        return self.quantity * self.supply.unit_sales_price
