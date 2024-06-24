from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Invoice(UUIDAutoFieldMixin, TimestampMixin):
    visit = models.OneToOneField("visits.Visit", on_delete=models.CASCADE)
    tax = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    sub_total = models.PositiveIntegerField(default=0, help_text="Total without tax and discount")

    @property
    def charges(self):
        item_charges = sum([item.charge for item in self.charge_items.all()])
        service_charges = sum([service.charge for service in self.charge_services.all()])
        return item_charges + service_charges

    @property
    def tax_amount(self):
        return self.charges * self.tax / 100

    @property
    def discount_amount(self):
        return self.charges * self.discount / 100

    @property
    def total(self):
        return self.charges + self.tax_amount - self.discount_amount

    @property
    def balance(self):
        return self.sub_total - self.total

    @property
    def label(self):
        return f"invoice#{self.uid.split('-')[-1]} | {self.visit.patient.get_full_name()}"

    def __str__(self):
        return f"{self.visit} | Tax: {self.tax} | Discount: {self.discount} | Subtotal: {self.sub_total}"

    class Meta:
        ordering = ("-created_at",)


class ChargeService(UUIDAutoFieldMixin, TimestampMixin):
    invoice = models.ForeignKey("invoices.Invoice", on_delete=models.CASCADE, related_name="charge_services")
    service = models.ForeignKey("healthcare.Service", on_delete=models.CASCADE, related_name="charge_services")

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("invoice", "service")

    @property
    def charge(self):
        return self.service.charge


class ChargeItem(UUIDAutoFieldMixin, TimestampMixin):
    invoice = models.ForeignKey("invoices.Invoice", on_delete=models.CASCADE, related_name="charge_items")
    supply = models.ForeignKey("inventory.Supply", on_delete=models.CASCADE, related_name="charge_items")
    quantity = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("invoice", "supply")

    @property
    def charge(self):
        return self.quantity * self.supply.unit_sales_price
