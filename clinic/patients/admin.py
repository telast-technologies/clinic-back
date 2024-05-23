from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from clinic.patients.models import Patient, PatientReport


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "first_name",
        "last_name",
        "email",
        "phone",
        "clinic",
        "birthdate",
        "address",
    ]
    search_fields = ["first_name", "last_name", "email", "phone"]
    list_filter = ("clinic",)

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False


@admin.register(PatientReport)
class PatientReportAdmin(admin.ModelAdmin):
    list_display = ["document", "patient", "created_at"]
    list_filter = ("created_at", "patient")

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
