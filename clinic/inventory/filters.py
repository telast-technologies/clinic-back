import django_filters

from clinic.inventory.models import Supply


class SupplyFilter(django_filters.FilterSet):
    class Meta:
        model = Supply
        fields = ("supply_type",)
