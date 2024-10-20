from rest_framework import serializers

from clinic.staff.models import Staff
from clinic.users.api.defaults import CurrentClinicDefault
from clinic.users.api.v1.serializers import PermissionDetailSerializer, UserDetailSerializer, UserModifySerializer


class StaffModifySerializer(serializers.ModelSerializer):
    user = UserModifySerializer()
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Staff
        fields = "__all__"
        extra_kwargs = {"permissions": {"required": False}}

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        user_data = validated_data.pop("user")
        user_serializer = self.fields["user"]
        # create user data
        user = user_serializer.create(user_data)
        validated_data["user"] = user
        # create utility staff
        staff = super().create(validated_data)
        staff.permissions.set(permissions)
        # return utility staff
        return staff

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions", None)
        user_data = validated_data.pop("user", None)
        user_serializer = self.fields["user"]

        if user_data:
            user_serializer.update(instance=instance.user, validated_data=user_data)

        if permissions:
            instance.permissions.set(permissions)

        return super().update(instance, validated_data)


class StaffListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Staff
        exclude = ["permissions"]


class StaffDetailSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())
    user = UserDetailSerializer(read_only=True)
    permissions = PermissionDetailSerializer(source="user.permissions", many=True, read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"
