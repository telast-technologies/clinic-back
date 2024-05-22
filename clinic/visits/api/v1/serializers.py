from rest_framework import serializers

from clinic.visits.models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"
