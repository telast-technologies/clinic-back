from django.core.validators import MinValueValidator
from django.db import models

from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Service(TimestampMixin, UUIDAutoFieldMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="services", editable=False
    )
    name = models.CharField(max_length=255)
    charge = models.FloatField(validators=[MinValueValidator(0.0)])
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("clinic", "name")

    def __str__(self):
        return self.name
