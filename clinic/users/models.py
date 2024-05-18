from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from clinic.users.choices import Roles
from clinic.utils.models import TimestampMixin, UUIDMixin


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
    def clinic(self):
        if hasattr(self, "staff"):
            return self.staff.clinic
        return None


class Staff(UUIDMixin, TimestampMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="staffs", db_index=True, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff",
        db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user.__str__()


class Patient(UUIDMixin, TimestampMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="patients", db_index=True, editable=False
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, unique=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
