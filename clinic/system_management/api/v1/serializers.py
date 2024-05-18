from rest_framework import serializers

from clinic.system_management.models import Clinic, Package


class PackageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ["name", "description", "price"]


class ClinicDetailSerializer(serializers.ModelSerializer):
    package = PackageDetailSerializer(read_only=True)

    class Meta:
        model = Clinic
        fields = "__all__"
