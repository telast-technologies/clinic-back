from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import RandomCharField

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
    staff_id = RandomCharField(
        length=16,
        help_text="Staff Code number",
        unique=True,
        include_alpha=False,
        include_punctuation=False,
        include_digits=True,
    )
    permissions = models.ManyToManyField("system_management.ExposedPermission", related_name="staff", blank=True)
    is_client_admin = models.BooleanField(_("Client Admin"), default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = _("Staff")
        permissions = (("change_clinic", "Can Change Clinic"),)

    def __str__(self) -> str:
        return self.user.__str__()
