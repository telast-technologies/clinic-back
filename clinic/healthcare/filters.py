import django_filters

from clinic.healthcare.models import Service


class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Service
        fields = ["name", "active", "created_at"]


class ServiceListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Service
        fields = ["name"]
