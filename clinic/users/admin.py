from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as auth_admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from clinic.users.models import User


@admin.register(User)
class UserAdmin(auth_admin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
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
        "phone",
        "is_superuser",
        "is_active",
        "date_joined",
    ]
    search_fields = ["first_name", "last_name"]
    list_filter = ("is_active", "date_joined")
    readonly_fields = ["last_login", "date_joined"]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).exclude(pk=request.user.pk)
