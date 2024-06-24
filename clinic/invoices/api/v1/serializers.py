from rest_framework import serializers

from clinic.healthcare.api.v1.serializers import ServiceDetailSerializer
from clinic.inventory.api.v1.serializers import SupplyDetailSerializer
from clinic.invoices.api.validators import ChargeItemValidator, ChargeServiceValidator
from clinic.invoices.models import ChargeItem, ChargeService, Invoice


class CreateChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = "__all__"
        validators = [ChargeItemValidator()]


class UpdateChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = ("uid", "quantity")


class ChargeItemDetailSerializer(serializers.ModelSerializer):
    supply = SupplyDetailSerializer(read_only=True)
    charge = serializers.FloatField(read_only=True)

    class Meta:
        model = ChargeItem
        exclude = ("invoice",)


class ChargeServiceModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeService
        fields = "__all__"
        validators = [ChargeServiceValidator()]


class ChargeServiceDetailSerializer(serializers.ModelSerializer):
    service = ServiceDetailSerializer(read_only=True)
    charge = serializers.FloatField(read_only=True)

    class Meta:
        model = ChargeService
        exclude = ("invoice",)


class InvoiceSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("visit",)


class SelectInvoiceSerializer(serializers.ModelSerializer):
    label = serializers.CharField(read_only=True)
    value = serializers.CharField(source="uid", read_only=True)

    class Meta:
        model = Invoice
        fields = ("label", "value")
