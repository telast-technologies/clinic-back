from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from clinic.healthcare.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "clinic",
        "name",
        "charge",
        "active",
    )
    list_filter = (
        "clinic",
        "active",
    )

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
