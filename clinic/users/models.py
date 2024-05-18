from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clinic.users.choices import Roles


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, unique=True)
    avatar = models.ImageField(upload_to="users", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "phone", "password"]

    def __str__(self) -> str:
        return self.get_full_name()

    @property
    def role(self):
        if hasattr(self, "staff"):
            return Roles.STAFF
        return Roles.OTHER

    @property
    def permissions(self):
        if hasattr(self, "staff") and self.staff.is_client_admin:
            return Permission.objects.filter(content_type__app_label__in=settings.ALLOWED_PERMISSIONS_APPS)
        if hasattr(self, "staff") and self.staff.is_client_admin:
            return Permission.objects.filter(id__in=self.staff.permissions.values_list("permission", flat=True))

        return Permission.objects.none()

    @property
    def clinic(self):
        if hasattr(self, "staff"):
            return self.staff.clinic
        return None
