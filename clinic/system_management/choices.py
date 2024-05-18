from django.db import models
from django.utils.translation import gettext_lazy as _


class PackageChoices(models.TextChoices):
    FREE_TRIAL = "free_trial", _("Free Trial")
    BASIC = "basic", _("Basic")
    PREMIUM = "premium", _("Premium")
    ONE_TIME_PAYMENT = "one_time_payment", _("One Time Payment")
