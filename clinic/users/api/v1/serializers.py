from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.system_management.api.v1.serializers import ClinicSerializer
from clinic.users.api.validators import PasswordValidator
from clinic.users.models import User


class PermissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("name", "codename")


class UserProfileSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    permissions = PermissionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "clinic",
            "avatar",
            "permissions",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "username",
            "is_active",
        )


class UserModifySerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        label=_("Password"),
        help_text=_("Password must be at least 8 characters long."),
        min_length=8,  # New validation for minimum length
    )
    password_confirm = serializers.CharField(
        write_only=True,
        label=_("Password confirmation"),
        help_text=_("Enter the same password as before, for verification."),
        min_length=8,  # New validation for minimum length
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "is_active",
            "password",
            "password_confirm",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
        validators = [PasswordValidator()]

    def create(self, validated_data):
        validated_data.pop("password_confirm", None)
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("password_confirm", None)
        password = validated_data.pop("password", None)
        if password:
            instance.password = make_password(password)
            instance.save()

        return super().update(instance=instance, validated_data=validated_data)
