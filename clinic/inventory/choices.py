from django.db import models
from django.utils.translation import gettext_lazy as _


class SupplyType(models.TextChoices):
    DRUG = "drug", _("Drug")
    SUPPLEMENT = "supplement", _("Supplement")
