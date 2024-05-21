from django.contrib import admin

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
        "quantity",
    )
    list_filter = ("clinic",)
