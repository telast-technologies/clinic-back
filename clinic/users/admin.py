from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as auth_admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from clinic.users.models import Patient, Staff, User


@admin.register(User)
class UserAdmin(auth_admin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "display_role",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = [
        "email",
        "get_full_name",
        "display_role",
        "phone",
        "is_superuser",
        "is_active",
        "date_joined",
    ]
    search_fields = ["first_name", "last_name"]
    list_filter = ("is_active", "date_joined")
    readonly_fields = ["last_login", "date_joined", "display_role"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).exclude(pk=request.user.pk)

    @admin.display(ordering="role")
    def display_role(self, obj: User) -> str:
        return obj.role


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "user",
        "clinic",
    ]
    search_fields = ["user__first_name", "user__last_name", "user__email", "user__phone"]
    list_filter = ("clinic",)

    def has_add_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any = None) -> bool:
        return False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).exclude(user=request.user)


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
