from django.db import models
from django.utils.translation import gettext_lazy as _


class InvoiceStatus(models.TextChoices):
    PAID = "PAID", _("Paid")
    PARTIAL_PAID = "PARTIAL_PAID", _("Partial Paid")
    UNPAID = "UNPAID", _("Unpaid")
    CANCELLED = "CANCELLED", _("Cancelled")
