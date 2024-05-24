from typing import Any

from django.contrib import admin
from django.http import HttpRequest
from fsm_admin2.admin import FSMTransitionMixin

from clinic.visits.models import ChargeItem, ChargeService, Visit


class ChargeItemInline(admin.TabularInline):
    model = ChargeItem
    fields = ["supply", "quantity"]
    extra = 0
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


class ChargeServiceInline(admin.TabularInline):
    model = ChargeService
    fields = ["service"]
    extra = 0
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


@admin.register(Visit)
class VisitAdmin(FSMTransitionMixin, admin.ModelAdmin):
    list_display = ["uid", "patient", "date", "time", "status"]
    list_filter = ["status", "date", "visit_type"]
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
