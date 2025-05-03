from django.db import models
from django.utils.translation import gettext_lazy as _


class StaffRoles(models.TextChoices):
    ADMIN = "admin", _("Admin")
    MANAGER = "manager", _("Manager")
    RECEPTIONIST = "receptionist", _("Receptionist")
    CALL_CENTER = "call_center", _("Call Center")
