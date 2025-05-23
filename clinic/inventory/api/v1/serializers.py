from rest_framework import serializers

from clinic.inventory.models import Supply
from clinic.users.api.defaults import CurrentClinicDefault


class SupplySerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())
    remains = serializers.FloatField(read_only=True)
    unit_sales_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Supply
        fields = "__all__"


class SupplyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ("uid", "item")


class SelectSupplySerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="item", read_only=True)
    value = serializers.CharField(source="uid", read_only=True)
    unit_sales_price = serializers.FloatField(read_only=True)
    remains = serializers.FloatField(read_only=True)

    class Meta:
        model = Supply
        fields = ("label", "value", "description", "unit_sales_price", "remains")
