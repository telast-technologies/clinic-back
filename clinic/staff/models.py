from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Staff(UUIDAutoFieldMixin, TimestampMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="staff", db_index=True, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff",
        db_index=True,
    )
    permissions = models.ManyToManyField("system_management.ExposedPermission", related_name="staff")
    is_client_admin = models.BooleanField(_("Client Admin"), default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = _("Staff")
        permissions = (("change_clinic", "Can Change Clinic"),)

    def __str__(self) -> str:
        return self.user.__str__()
