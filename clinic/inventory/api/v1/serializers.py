from rest_framework import serializers

from clinic.inventory.models import Supply
from clinic.users.api.defaults import CurrentClinicDefault


class SupplySerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Supply
        fields = "__all__"
