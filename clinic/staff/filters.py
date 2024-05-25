import django_filters

from clinic.staff.models import Staff


class StaffFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        field_name="user__is_active",
        label="Filter by active Status",
    )
    fullname = django_filters.CharFilter(
        method="filter_fullname",
        lookup_expr="icontains",
        label="Can Search by Fullname that contains",
    )

    class Meta:
        model = Staff
        fields = ["uid", "is_active", "fullname", "is_client_admin"]

    def filter_fullname(self, queryset, name, value):
        return queryset.filter(user__first_name__icontains=value) | queryset.filter(user__last_name__icontains=value)
