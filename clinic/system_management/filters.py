import django_filters

from clinic.system_management.models import ExposedPermission


class PermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="permission__name",
        lookup_expr="icontains",
        label="Admin Staff can filter by permission name matches by containing this string",
    )

    class Meta:
        model = ExposedPermission
        fields = ["name"]
