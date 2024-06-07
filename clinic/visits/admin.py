from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from clinic.visits.models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["uid", "status", "patient", "date", "time"]
    list_filter = ["date", "visit_type", "status"]
    search_fields = ["uid"]

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False
