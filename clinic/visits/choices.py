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


class VisitStatus(models.TextChoices):
    BOOKED = "booked", _("Booked")
    CHECKED_IN = "checked_in", _("Checked In")
    FINANCIALLY_CLEARED = "financially_cleared", _("Financially Cleared")
    CHECKED_OUT = "checked_out", _("Checked Out")
    CANCELLED = "cancelled", _("Cancelled")


class VisitType(models.TextChoices):
    SCHEDULED = "scheduled", _("Scheduled")
    WALK_IN = "walk_in", _("Walk In")


class TimeChoices(models.TextChoices):
    UPCOMING = "upcoming", _("Up Coming")
    PAST = "past", _("Pasr")
    ALL = "all", _("All")
