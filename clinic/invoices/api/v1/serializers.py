from rest_framework import serializers

from clinic.invoices.models import Invoice
from clinic.visits.api.v1.serializers import ChargeItemDetailSerializer, ChargeServiceDetailSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    charge_items = ChargeItemDetailSerializer(source="visit.charge_items", many=True, read_only=True)
    charge_services = ChargeServiceDetailSerializer(source="visit.charge_services", many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("visit",)
