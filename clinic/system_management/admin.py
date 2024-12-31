from django.contrib import admin

from clinic.system_management.admin_actions import ClinicActivationAdminAction, PackageActivationAdminAction
from clinic.system_management.forms import ExposedPermissionForm
from clinic.system_management.models import Clinic, ExposedPermission, Package
from clinic.visits.models import TimeSlot


@admin.register(Package)
class PackageAdmin(PackageActivationAdminAction, admin.ModelAdmin):
    actions = ["activate", "deactivate"]
    list_display = ("uid", "name", "description", "price", "active")
    list_filter = ("active",)
    search_fields = ("name", "uid")
    ordering = ("name",)


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 0
    fields = ("start_time", "end_time", "days")


@admin.register(Clinic)
class ClinicAdmin(ClinicActivationAdminAction, admin.ModelAdmin):
    list_display = (
        "uid",
        "name",
        "package",
        "website",
        "active",
    )
    actions = ["activate", "deactivate"]
    list_filter = ("package", "active")
    search_fields = ("name", "uid", "address", "phone", "email", "website")
    inlines = [TimeSlotInline]
    ordering = ("name",)


@admin.register(ExposedPermission)
class ExposedPermissionAdmin(admin.ModelAdmin):
    form = ExposedPermissionForm
    list_display = ["permission", "created_at"]
    search_fields = ("permission__name",)
