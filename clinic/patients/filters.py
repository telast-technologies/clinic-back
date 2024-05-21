import django_filters

from clinic.patients.models import Patient


class PatientFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(
        method="filter_fullname",
    )
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Patient
        fields = ["uid", "fullname", "phone", "email", "created_at"]

    def filter_fullname(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value) | queryset.filter(last_name__icontains=value)
