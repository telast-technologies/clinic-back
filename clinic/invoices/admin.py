from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from clinic.invoices.models import ChargeItem, ChargeService, Invoice


class ChargeItemInline(admin.TabularInline):
    model = ChargeItem
    fields = ("supply", "quantity", "charge", "remains")
    readonly_fields = ("charge", "remains")
    extra = 0
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    @admin.display(description="charge")
    def charge(self, obj: ChargeItem) -> float:
        return obj.charge

    @admin.display(description="remains")
    def remains(self, obj: ChargeItem) -> float:
        return obj.supply.remains


class ChargeServiceInline(admin.TabularInline):
    model = ChargeService
    fields = ("service", "charge")
    extra = 0
    can_delete = False
    readonly_fields = ("charge",)

    @admin.display(description="charge")
    def charge(self, obj: ChargeService) -> float:
        return obj.charge

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("visit", "tax", "discount", "sub_total", "total", "balance")
    readonly_fields = ["total", "balance"]
    search_fields = ["visit__uid"]
    inlines = [ChargeItemInline, ChargeServiceInline]

    @admin.display(description="balance")
    def balance(self, obj):
        return obj.balance

    @admin.display(description="total")
    def total(self, obj):
        return obj.total

    def has_add_permission(self, request: HttpRequest, obj: Invoice = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Invoice = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Invoice = None) -> bool:
        return False
