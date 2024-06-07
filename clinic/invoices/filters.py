import django_filters

from clinic.invoices.models import ChargeItem, ChargeService, Invoice


class InvoiceFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Invoice
        fields = ("visit", "uid", "created_at")


class ChargeItemFilter(django_filters.FilterSet):
    invoice = django_filters.ModelChoiceFilter(queryset=Invoice.objects.all(), field_name="invoice", required=True)

    class Meta:
        model = ChargeItem
        fields = ("uid", "invoice", "supply")


class ChargeServiceFilter(django_filters.FilterSet):
    invoice = django_filters.ModelChoiceFilter(queryset=Invoice.objects.all(), field_name="invoice", required=True)

    class Meta:
        model = ChargeService
        fields = ("uid", "invoice", "service")