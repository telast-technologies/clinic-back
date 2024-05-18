from rest_framework import serializers

from clinic.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "fullname",
            "phone",
            "avatar",
        ]
