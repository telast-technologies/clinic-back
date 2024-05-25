from django.utils import timezone
from rest_framework import serializers

from clinic.healthcare.api.v1.serializers import ServiceDetailSerializer
from clinic.inventory.api.v1.serializers import SupplyDetailSerializer
from clinic.patients.api.v1.serializers import PatientSerializer
from clinic.users.api.defaults import CurrentClinicDefault
from clinic.visits.api.v1.validators import ChargeItemValidator, ChargeServiceValidator, VisitValidator
from clinic.visits.choices import VisitType
from clinic.visits.models import ChargeItem, ChargeService, TimeSlot, Visit


class TimeSlotSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = TimeSlot
        fields = "__all__"


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

    class Meta:
        model = Visit
        fields = "__all__"


class SelectVisitSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="uid", read_only=True)
    value = serializers.CharField(source="uid", read_only=True)

    class Meta:
        model = Visit
        fields = ["label", "value"]


class CreateChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = "__all__"
        validators = [ChargeItemValidator()]


class UpdateChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = ["quantity"]


class ChargeItemDetailSerializer(serializers.ModelSerializer):
    supply = SupplyDetailSerializer(read_only=True)
    charge = serializers.FloatField(read_only=True)

    class Meta:
        model = ChargeItem
        fields = "__all__"


class ChargeServiceModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeService
        fields = "__all__"
        validators = [ChargeServiceValidator()]


class ChargeServiceDetailSerializer(serializers.ModelSerializer):
    service = ServiceDetailSerializer(read_only=True)
    charge = serializers.FloatField(read_only=True)

    class Meta:
        model = ChargeService
        fields = "__all__"


class AvailableSlotListSerializer(serializers.Serializer):
    slots = serializers.ListField(child=serializers.TimeField())


class AvailableDateListSerializer(serializers.Serializer):
    dates = serializers.ListField(child=serializers.DateField())
