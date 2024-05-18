from django.contrib import admin

from clinic.system_management.forms import ExposedPermissionForm
from clinic.system_management.models import Clinic, ExposedPermission, Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "description", "price", "active")


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "name",
        "package",
        "address",
        "phone",
        "email",
        "website",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(ExposedPermission)
class ExposedPermissionAdmin(admin.ModelAdmin):
    form = ExposedPermissionForm
    list_display = ["permission", "created_at"]
    search_fields = ("permission__name",)
