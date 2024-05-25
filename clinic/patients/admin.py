from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from clinic.patients.models import Patient, PatientReport


class PatientReportInline(admin.TabularInline):
    model = PatientReport
    extra = 0
    fields = ("document",)
    can_delete = False

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "first_name",
        "last_name",
        "email",
        "phone",
        "clinic",
    ]
    search_fields = ["first_name", "last_name", "email", "phone"]
    list_filter = ("clinic",)
    inlines = [PatientReportInline]

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
