import humanize
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django_extensions.db.fields import RandomCharField
from phonenumber_field.modelfields import PhoneNumberField

from clinic.patients.choices import Channels, GenderChoices
from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Patient(UUIDAutoFieldMixin, TimestampMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="patients", db_index=True, editable=False
    )
    medical_number = RandomCharField(
        length=6,
        help_text="medical number",
        unique=True,
        include_alpha=False,
        include_punctuation=False,
        include_digits=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION)
    birthdate = models.DateTimeField(null=True, blank=True)
    country = CountryField(default="EG")
    address = models.CharField(max_length=100, default="", blank=True)
    nid = models.CharField(max_length=14, help_text="National ID", default="", blank=True)
    passport = models.CharField(max_length=10, help_text="Passport ID", default="", blank=True)
    channel = models.CharField(max_length=100, choices=Channels.choices)
    other_channel = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_patient_email", nulls_distinct=True),
        ]

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        return (timezone.now() - self.birthdate).days // 365 if self.birthdate else 0

    def __str__(self) -> str:
        return self.get_full_name()


class PatientReport(UUIDAutoFieldMixin, TimestampMixin):
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="reports",
        db_index=True,
    )
    document = models.FileField(upload_to="patients/reports")

    @property
    def filename(self):
        return self.document.name.split("/")[-1] if self.document else ""

    @property
    def size(self):
        return humanize.naturalsize(self.document.size) if self.document else ""

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.document.url if self.document else '-'}"


class PatientPrescription(UUIDAutoFieldMixin, TimestampMixin):
    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="prescriptions",
        db_index=True,
    )
    examination = models.TextField()
    medicines = ArrayField(models.JSONField(), null=True, blank=True)
    notes = models.TextField(default="", blank=True)

    def __str__(self) -> str:
        return f"Prescription for {self.patient.get_full_name()}"
