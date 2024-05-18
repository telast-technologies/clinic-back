from django.db import models
from django.utils.translation import gettext_lazy as _


class JoinRequestStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    APPROVED = "approved", _("Approved")
    REJECTED = "rejected", _("Rejected")
