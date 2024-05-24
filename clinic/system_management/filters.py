import django_filters

from clinic.system_management.models import ExposedPermission, Package


class SelectPackageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="anyone can filter by package name matches by containing this string",
    )

    class Meta:
        model = Package
        fields = ["name"]


class SelectPermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="permission__name",
        lookup_expr="icontains",
        label="Admin Staff can filter by permission name matches by containing this string",
    )

    class Meta:
        model = ExposedPermission
        fields = ["name"]
