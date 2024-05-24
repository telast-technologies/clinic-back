from typing import Any

from django.contrib import admin
from django.http import HttpRequest
from fsm_admin2.admin import FSMTransitionMixin

from clinic.visits.models import ChargeItem, ChargeService, Visit


class ChargeItemInline(admin.TabularInline):
    model = ChargeItem
    fields = ["supply", "quantity", "charge", "remains"]
    readonly_fields = ["charge", "remains"]
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
    fields = ["service", "charge"]
    extra = 0
    can_delete = False
    readonly_fields = ["charge"]

    @admin.display(description="charge")
    def charge(self, obj: ChargeService) -> float:
        return obj.charge

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


@admin.register(Visit)
class VisitAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ["uid", "patient", "date", "time", "status"]
    list_filter = ["status", "date", "visit_type"]
    search_fields = ["uid"]
    fsm_fields = [
        "status",
    ]  # list your fsm fields
    inlines = [ChargeItemInline, ChargeServiceInline]
    # you can override templates for transition arguments form view and transition buttons row
    fsm_transition_form_template = "fsm_admin2/fsm_transition_form.html"  # default value
    fsm_transition_buttons_template = "fsm_admin2/fsm_transition_buttons.html"  # default value

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
