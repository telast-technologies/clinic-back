from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from django_extensions.db.fields import RandomCharField

from clinic.inventory.choices import SupplyType
from clinic.inventory.managers import SupplyManager
from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Supply(TimestampMixin, UUIDAutoFieldMixin):
    clinic = models.ForeignKey(
        "system_management.Clinic", on_delete=models.CASCADE, related_name="supplies", editable=False
    )
    no = RandomCharField(
        length=6,
        help_text="Supply number",
        unique=True,
        include_alpha=False,
        include_punctuation=False,
        include_digits=True,
    )
    invoice = models.SmallIntegerField(validators=[MinValueValidator(0)])
    item = models.CharField(max_length=255)
    description = models.TextField(default="")
    supply_type = models.CharField(max_length=10, choices=SupplyType.choices)
    unit_cost = models.FloatField(validators=[MinValueValidator(0.0)])
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])
    charge = models.GeneratedField(
        expression=F("unit_cost") * F("quantity"),
        output_field=models.FloatField(validators=[MinValueValidator(0.0)]),
        db_persist=True,
    )
    lot = RandomCharField(
        length=8,
        help_text="Lot number",
        unique=True,
        include_alpha=False,
        include_punctuation=False,
        include_digits=True,
    )
    expires_at = models.DateTimeField()
    qrcode = RandomCharField(length=160, editable=False, unique=True)

    objects = SupplyManager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name_plural = "supplies"

    def __str__(self):
        return self.item

    @property
    def label(self):
        return f"{self.item} ({self.lot})"

    @property
    def unit_sales_price(self):
        price = self.unit_cost + (self.unit_cost * (self.clinic.profit_share / 100))
        return price if self.supply_type == SupplyType.SUPPLEMENT else self.unit_cost

    @property
    def remains(self):
        value = (
            self.quantity
            - self.charge_items.aggregate(charge_quantity=Coalesce(Sum("quantity"), Value(0.0)))["charge_quantity"]
        )
        return value if value >= 0.0 else 0.0
