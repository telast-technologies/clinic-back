from django.db import models
from django_extensions.db.fields import ShortUUIDField


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDAutoFieldMixin(models.Model):
    uid = ShortUUIDField(primary_key=True, editable=False)

    class Meta:
        abstract = True
