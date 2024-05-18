from django.contrib import admin

from clinic.system_management.models import Clinic, Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "description", "price")


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
