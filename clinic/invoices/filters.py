import django_filters

from clinic.invoices.models import Invoice


class InvoiceFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Invoice
        fields = ("visit", "uid", "created_at")
