from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from clinic.utils.models import TimestampMixin, UUIDMixin


class Supply(TimestampMixin, UUIDMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="supplies", editable=False
    )
    invoice = models.SmallIntegerField(validators=[MinValueValidator(0)])
    item = models.CharField(max_length=255)
    charge = models.FloatField(validators=[MinValueValidator(0.0)])
    profit_share = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    unit_cost = models.FloatField(validators=[MinValueValidator(0.0)])
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "supplies"

    def __str__(self):
        return self.item
