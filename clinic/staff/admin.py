from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from clinic.staff.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "user",
        "clinic",
        "is_client_admin",
    ]
    search_fields = ["user__first_name", "user__last_name", "user__email", "user__phone"]
    list_filter = ("clinic", "is_client_admin")

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).exclude(user=request.user)
