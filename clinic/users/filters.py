import django_filters

from clinic.users.models import Patient, Staff


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
        fields = ["uid", "is_active", "fullname", "clinic"]

    def filter_fullname(self, queryset, name, value):
        return queryset.filter(user__first_name__icontains=value) | queryset.filter(user__last_name__icontains=value)


class PatientFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter(
        method="filter_fullname",
    )

    class Meta:
        model = Patient
        fields = ["uid", "fullname", "clinic", "phone"]

    def filter_fullname(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value) | queryset.filter(last_name__icontains=value)
