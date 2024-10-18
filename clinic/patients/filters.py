import django_filters

from clinic.patients.models import Patient, PatientReport


class PatientFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Patient
        fields = ("created_at", "channel")


class PatientReportFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = PatientReport
        fields = ("patient", "created_at")
