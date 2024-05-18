from rest_framework import serializers

from clinic.system_management.models import Clinic, ExposedPermission, Package


class ClinicSerializer(serializers.ModelSerializer):
    package = serializers.CharField(source="package.name", read_only=True)

    class Meta:
        model = Clinic
        exclude = ("uid", "created_at", "updated_at")


class PackageSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="uid", read_only=True)
    label = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = Package
        fields = ("value", "label")


class ExposedPermissionSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="uid", read_only=True)
    label = serializers.CharField(source="permission.name", read_only=True)

    class Meta:
        model = ExposedPermission
        fields = ["label", "value"]
