from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from clinic.inventory.models import Supply


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = (
        "clinic",
        "invoice",
        "item",
        "charge",
        "profit_share",
        "unit_cost",
        "unit_sales_price",
        "quantity",
        "remains",
    )
    list_filter = ("clinic",)
    readonly_fields = ("charge", "unit_sales_price", "remains")
    search_fields = ("item", "invoice", "clinic", "uid")

    @admin.display(description="remains")
    def remains(self, obj: Supply) -> float:
        return obj.remains

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
