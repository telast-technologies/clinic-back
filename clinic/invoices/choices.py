from django.db import models
from django.utils.translation import gettext_lazy as _


class InvoiceStatus(models.TextChoices):
    PAID = "paid", _("Paid")
    PARTIAL_PAID = "partial_paid", _("Partial Paid")
    UNPAID = "unpaid", _("Unpaid")
    CANCELLED = "cancelled", _("Cancelled")
