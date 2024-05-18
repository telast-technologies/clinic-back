from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.system_management.api.v1.serializers import ClinicSerializer
from clinic.users.models import User


class PermissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["name", "codename"]


class UserProfileSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    permissions = PermissionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "clinic",
            "avatar",
            "permissions",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
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

    def validate(self, data):
        data = super().validate(data)
        request_method = self.context.get("request").method
        # Check if password and password_confirm are provided
        password = data.get("password", None)
        password_confirm = data.pop("password_confirm", None)

        if any(
            [
                request_method == "POST" and not (password and password_confirm),
                request_method in ["PATCH", "PUT"] and (password and not password_confirm),
                request_method in ["PATCH", "PUT"] and (not password and password_confirm),
                (password and password_confirm) and password != password_confirm,
            ]
        ):
            raise serializers.ValidationError({"password": _("invalid or missing password")})

        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data=validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.password = make_password(password)
            instance.save()

        return super().update(instance=instance, validated_data=validated_data)
