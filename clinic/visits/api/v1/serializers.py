from django.utils import timezone
from rest_framework import serializers

from clinic.patients.api.v1.serializers import PatientSerializer
from clinic.users.api.defaults import CurrentClinicDefault
from clinic.visits.api.validators import TimeSlotValidator, VisitValidator
from clinic.visits.choices import VisitType
from clinic.visits.models import TimeSlot, Visit


class TimeSlotSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = TimeSlot
        fields = "__all__"

        validators = [TimeSlotValidator()]


class CreateVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"
        read_only_fields = ["status"]

        validators = [VisitValidator()]

    def create(self, validated_data):
        visit_type = validated_data.get("visit_type")
        if visit_type == VisitType.WALK_IN:
            validated_data["date"] = timezone.now().date()
            validated_data["time"] = timezone.now().time()

        return super().create(validated_data)


class UpdateVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"
        read_only_fields = ["status", "visit_type", "patient"]

        validators = [VisitValidator()]

    def update(self, instance, validated_data):
        if instance.visit_type == VisitType.WALK_IN:
            return instance

        return super().update(instance, validated_data)


class VisitDetailSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    invoice = serializers.CharField(source="invoice.uid", read_only=True)

    class Meta:
        model = Visit
        fields = "__all__"


class AvailableSlotListSerializer(serializers.Serializer):
    slots = serializers.ListField(child=serializers.TimeField())


class AvailableDateListSerializer(serializers.Serializer):
    dates = serializers.ListField(child=serializers.DateField())


class VisitCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ("uid", "date", "time", "status")
