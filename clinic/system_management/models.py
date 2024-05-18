from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clinic.system_management.choices import PackageChoices
from clinic.utils.models import TimestampMixin, UUIDMixin


class Package(UUIDMixin, TimestampMixin):
    name = models.CharField(max_length=100, unique=True, choices=PackageChoices.choices)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Clinic(UUIDMixin, TimestampMixin):
    package = models.ForeignKey("Package", on_delete=models.RESTRICT, related_name="clinics")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class ExposedPermission(UUIDMixin, TimestampMixin):
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.permission.name
