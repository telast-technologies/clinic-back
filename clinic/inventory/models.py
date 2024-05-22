from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F

from clinic.utils.models import TimestampMixin, UUIDMixin


class Supply(TimestampMixin, UUIDMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="supplies", editable=False
    )
    invoice = models.SmallIntegerField(validators=[MinValueValidator(0)])
    item = models.CharField(max_length=255)
    profit_share = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    unit_cost = models.FloatField(validators=[MinValueValidator(0.0)])
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])
    unit_sales_price = models.GeneratedField(
        expression=F("unit_cost") + (F("unit_cost") * (F("profit_share") / 100)),
        output_field=models.FloatField(validators=[MinValueValidator(0.0)]),
        db_persist=True,
    )
    charge = models.GeneratedField(
        expression=F("unit_cost") * F("quantity"),
        output_field=models.FloatField(validators=[MinValueValidator(0.0)]),
        db_persist=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "supplies"

    def __str__(self):
        return self.item
