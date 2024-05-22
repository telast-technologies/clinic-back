from django.db import models
from django.utils.translation import gettext_lazy as _


class DaysOfWeek(models.TextChoices):
    MONDAY = "monday", _("Monday")
    TUESDAY = "tuesday", _("Tuesday")
    WEDNESDAY = "wednesday", _("Wednesday")
    THURSDAY = "thursday", _("Thursday")
    FRIDAY = "friday", _("Friday")
    SATURDAY = "saturday", _("Saturday")
    SUNDAY = "sunday", _("Sunday")
