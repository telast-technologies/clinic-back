import django_filters

from clinic.healthcare.models import Service


class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = ("active",)
