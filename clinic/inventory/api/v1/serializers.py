from rest_framework import serializers

from clinic.inventory.models import Supply
from clinic.users.api.defaults import CurrentClinicDefault


class SupplySerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())
    remain = serializers.FloatField(read_only=True)

    class Meta:
        model = Supply
        fields = "__all__"


class SupplyDetailSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Supply
        exclude = ["qrcode", "quantity"]


class SelectSupplySerializer(serializers.ModelSerializer):
    label = serializers.CharField(read_only=True)
    value = serializers.CharField(source="uid", read_only=True)

    class Meta:
        model = Supply
        fields = ["label", "value"]
