import django_filters

from clinic.inventory.models import Supply


class SupplyFilter(django_filters.FilterSet):
    invoice = django_filters.CharFilter(field_name="invoice", lookup_expr="icontains")
    item = django_filters.CharFilter(field_name="item", lookup_expr="icontains")
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Supply
        fields = ("item", "invoice", "created_at")


class SelectSupplyFilter(django_filters.FilterSet):
    item = django_filters.CharFilter(field_name="item", lookup_expr="icontains")

    class Meta:
        model = Supply
        fields = ("item",)
