from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clinic.utils.models import TimestampMixin, UUIDMixin


class Package(UUIDMixin, TimestampMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Clinic(UUIDMixin, TimestampMixin):
    package = models.ForeignKey("Package", on_delete=models.RESTRICT, related_name="clinics")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
