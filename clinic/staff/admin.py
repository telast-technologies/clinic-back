from django.contrib import admin

from clinic.staff.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "user",
        "clinic",
        "staff_id",
        "is_client_admin",
    ]
    search_fields = ["user__first_name", "user__last_name", "user__email", "user__phone"]
    list_filter = ("clinic", "is_client_admin")
