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
    permissions = PermissionDetailSerializer(source="user.permissions", many=True, read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"


class StaffListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = "__all__"
