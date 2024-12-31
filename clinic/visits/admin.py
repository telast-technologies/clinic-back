from django.contrib import admin

from clinic.visits.models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["uid", "status", "patient", "date", "time"]
    list_filter = ["date", "visit_type", "status"]
    search_fields = ["uid", "no"]
