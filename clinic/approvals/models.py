from django.conf import settings
from django.db import models
from model_utils import FieldTracker
from phonenumber_field.modelfields import PhoneNumberField

from clinic.approvals.choices import JoinRequestStatusChoices
from clinic.system_management.validators import PackageActiveStatusValidator
from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class JoinRequest(UUIDAutoFieldMixin, TimestampMixin):
    administrator_first_name = models.CharField(max_length=100)
    administrator_last_name = models.CharField(max_length=100)
    administrator_email = models.EmailField()
    administrator_phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION)
    clinic_name = models.CharField(max_length=100)
    clinic_description = models.TextField(null=True, blank=True)
    clinic_address = models.CharField(max_length=100, null=True, blank=True)
    clinic_phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, null=True, blank=True)
    clinic_email = models.EmailField(null=True, blank=True)
    clinic_website = models.URLField(null=True, blank=True)
    package = models.ForeignKey(
        "system_management.Package",
        on_delete=models.CASCADE,
        related_name="join_requests",
        validators=[PackageActiveStatusValidator()],
    )
    status = models.CharField(
        max_length=100, choices=JoinRequestStatusChoices.choices, default=JoinRequestStatusChoices.PENDING
    )

    tracker = FieldTracker()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.administrator_first_name} {self.administrator_last_name}"
