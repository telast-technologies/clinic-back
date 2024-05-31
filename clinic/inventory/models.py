from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from django_extensions.db.fields import RandomCharField

from clinic.inventory.managers import SupplyManager
from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Supply(TimestampMixin, UUIDAutoFieldMixin):
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
    qrcode = RandomCharField(length=160, editable=False, unique=True)

    objects = SupplyManager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "supplies"

    def __str__(self):
        return self.item

    @property
    def label(self):
        return f"{self.item} ({self.unit_sales_price})"

    @property
    def remains(self):
        value = (
            self.quantity
            - self.charge_items.aggregate(charge_quantity=Coalesce(Sum("quantity"), Value(0.0)))["charge_quantity"]
        )
        return value if value >= 0.0 else 0.0
