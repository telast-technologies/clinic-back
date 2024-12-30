from django.contrib import admin

from clinic.inventory.models import Supply


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = (
        "clinic",
        "invoice",
        "item",
        "description",
        "supply_type",
        "charge",
        "lot",
        "unit_cost",
        "unit_sales_price",
        "quantity",
        "remains",
    )
    list_filter = ("clinic",)
    readonly_fields = ("charge", "lot", "remains")
    search_fields = ("item", "invoice", "clinic", "uid", "lot")
