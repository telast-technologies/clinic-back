from rest_framework import serializers

from clinic.approvals.models import JoinRequest


class JoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinRequest
        exclude = ("status",)
