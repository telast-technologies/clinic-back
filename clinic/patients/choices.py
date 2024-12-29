from django.db import models
from django.utils.translation import gettext_lazy as _


class Channels(models.TextChoices):
    FACEBOOK = "facebook", _("Facebook")
    INSTAGRAM = "instagram", _("Instagram")
    TWITTER = "twitter", _("Twitter")
    LINKEDIN = "linkedin", _("Linkedin")
    YOUTUBE = "youtube", _("Youtube")
    TIKTOK = "tiktok", _("Tiktok")
    SNAPCHAT = "snapchat", _("Snapchat")
    TELEGRAM = "telegram", _("Telegram")
    WHATSAPP = "whatsapp", _("Whatsapp")
    SMS = "sms", _("SMS")
    EMAIL = "email", _("Email")
    OTHER = "other", _("Other")


class GenderChoices(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
