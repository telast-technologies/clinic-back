from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, null=True, blank=True)
    avatar = models.ImageField(upload_to="users", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password"]

    def __str__(self) -> str:
        return self.get_full_name()
