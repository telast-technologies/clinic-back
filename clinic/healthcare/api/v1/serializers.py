from rest_framework import serializers

from clinic.healthcare.models import Service
from clinic.users.api.defaults import CurrentClinicDefault


class ServiceSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Service
        fields = "__all__"


class ServiceListSelectSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="name")
    value = serializers.CharField(source="uid")

    class Meta:
        model = Service
        fields = ("label", "value")
