import django_filters

from clinic.invoices.models import ChargeItem, ChargeService, Invoice


class InvoiceFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")
    due_date = django_filters.DateFromToRangeFilter(field_name="due_date")

    class Meta:
        model = Invoice
        fields = ("visit", "created_at", "due_date")


class ChargeItemFilter(django_filters.FilterSet):
    class Meta:
        model = ChargeItem
        fields = ("invoice", "supply")


class ChargeServiceFilter(django_filters.FilterSet):
    class Meta:
        model = ChargeService
        fields = ("invoice", "service")
