from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.users.api.defaults import CurrentClinicDefault
from clinic.users.models import Patient, Staff, User


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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar",
        ]


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


class StaffModifySerializer(serializers.ModelSerializer):
    user = UserModifySerializer()
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Staff
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = self.fields["user"]
        # create user data
        user = user_serializer.create(user_data)
        validated_data["user"] = user
        # create utility staff
        staff = super().create(validated_data)
        # return utility staff
        return staff

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        user_serializer = self.fields["user"]

        if user_data:
            user_serializer.update(instance=instance.user, validated_data=user_data)

        return super().update(instance, validated_data)


class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Patient
        fields = "__all__"
