import django_filters

from clinic.patients.models import Patient, PatientPrescription, PatientReport


class PatientFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Patient
        fields = ("created_at", "channel", "country", "gender")


class PatientReportFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = PatientReport
        fields = ("patient", "created_at")


class PatientPrescriptionFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = PatientPrescription
        fields = ("patient", "created_at")
