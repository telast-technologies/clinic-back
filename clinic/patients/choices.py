from django.db import models
from django.utils.translation import gettext_lazy as _


class Channels(models.TextChoices):
    FACEBOOK = "facebook", _("Facebook")
    TELEGRAM = "telegram", _("Telegram")
    WHATSAPP = "whatsapp", _("Whatsapp")
    SMS = "sms", _("SMS")
    EMAIL = "email", _("Email")
    OTHER = "other", _("Other")
