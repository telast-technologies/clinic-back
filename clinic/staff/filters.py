import django_filters

from clinic.staff.models import Staff


class StaffFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        field_name="user__is_active",
        label="Filter by active Status",
    )

    class Meta:
        model = Staff
        fields = ("is_active", "is_client_admin")
