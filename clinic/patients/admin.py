from django.contrib import admin

from clinic.patients.models import Patient, PatientPrescription, PatientReport


class PatientReportInline(admin.TabularInline):
    model = PatientReport
    extra = 0
    fields = ("document",)


class PatientPrescriptionInline(admin.TabularInline):
    model = PatientPrescription
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "medical_number",
        "first_name",
        "last_name",
        "email",
        "phone",
        "clinic",
    ]
    search_fields = ["first_name", "last_name", "email", "phone"]
    list_filter = ("clinic",)
    inlines = [PatientReportInline, PatientPrescriptionInline]
