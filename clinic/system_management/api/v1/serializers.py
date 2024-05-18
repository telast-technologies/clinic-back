from rest_framework import serializers

from clinic.system_management.models import Clinic


class ClinicDetailSerializer(serializers.ModelSerializer):
    package = serializers.CharField(source="package.name", read_only=True)

    class Meta:
        model = Clinic
        fields = "__all__"
