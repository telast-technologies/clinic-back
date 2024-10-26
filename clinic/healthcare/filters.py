import django_filters

from clinic.healthcare.models import Service


class ServiceFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Service
        fields = ("active", "created_at")
