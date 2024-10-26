from django.contrib import admin

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
        "active",
        "clinic",
    )
    search_fields = ("name", "uid")
