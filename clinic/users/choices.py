from django.db import models
from django.utils.translation import gettext_lazy as _


class Roles(models.TextChoices):
    STAFF = "staff", _("Staff")
    OTHER = "other", _("Other")
