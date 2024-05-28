from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from clinic.visits.models import ChargeItem, ChargeService, Visit


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


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["uid", "status", "patient", "date", "time"]
    list_filter = ["date", "visit_type", "status"]
    search_fields = ["uid"]
    inlines = [ChargeItemInline, ChargeServiceInline]

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
