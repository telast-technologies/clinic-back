from django.conf import settings
from django.db import models

from clinic.utils.models import TimestampMixin, UUIDMixin


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
    permissions = models.ManyToManyField("system_management.ExposedPermission", related_name="staff")
    is_client_admin = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.user.__str__()
