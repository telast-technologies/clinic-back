from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clinic.patients.choices import Channels
from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Patient(UUIDAutoFieldMixin, TimestampMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="patients", db_index=True, editable=False
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, unique=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    nid = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, choices=Channels.choices)

    class Meta:
        ordering = ("-created_at",)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.get_full_name()}"


class PatientReport(UUIDAutoFieldMixin, TimestampMixin):
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="reports",
        db_index=True,
    )
    document = models.FileField(upload_to="patients/reports")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.document.url if self.document else '-'}"
