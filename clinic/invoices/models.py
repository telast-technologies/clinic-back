from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Invoice(UUIDAutoFieldMixin, TimestampMixin):
    visit = models.OneToOneField("visits.Visit", on_delete=models.CASCADE)
    tax = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    sub_total = models.PositiveIntegerField(default=0, help_text="Total without tax and discount")

    @property
    def tax_amount(self):
        return self.sub_total * self.tax / 100
    
    @property
    def discount_amount(self):
        return self.sub_total * self.discount / 100

    @property
    def total(self):
        return self.sub_total + self.tax_amount - self.discount_amount
        
    @property
    def balance(self):
        return self.total - self.visit.charges
    
    
    def __str__(self):
        return f"{self.visit} | Tax: {self.tax} | Discount: {self.discount} | Subtotal: {self.sub_total}"
    class Meta:
        ordering = ("-created_at",)