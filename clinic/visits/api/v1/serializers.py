from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.healthcare.api.v1.serializers import ServiceDetailSerializer
from clinic.inventory.api.v1.serializers import SupplyDetailSerializer
from clinic.patients.api.v1.serializers import PatientSerializer
from clinic.system_management.services.clinic_service import ClinicService
from clinic.users.api.defaults import CurrentClinicDefault
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

    def validate(self, attrs):
        data = super().validate(attrs)
        visit_type = data.get("visit_type")
        date = data.get("date")
        time = data.get("time")

        if any(
            [
                data["patient"].clinic != self.context["request"].user.staff.clinic,
                visit_type == VisitType.SCHEDULED
                and time not in ClinicService(self.context["request"].user.staff.clinic).get_available_slots(date),
            ]
        ):
            raise serializers.ValidationError({"visit": _("invalid or missing visit data")})

        return data

    def create(self, validated_data):
        visit_type = validated_data.get("visit_type")
        if visit_type == VisitType.WALK_IN:
            validated_data["time"] = timezone.now().time()
        return super().create(validated_data)


class UpdateVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"
        read_only_fields = ["status", "visit_type", "patient"]

    def validate(self, attrs, *args, **kwargs):
        data = super().validate(attrs, *args, **kwargs)

        date = data.get("date", self.instance.date)
        time = data.get("time", self.instance.time)

        if any(
            [
                self.instance.visit_type == VisitType.SCHEDULED
                and (date or time)
                and time not in ClinicService(self.context["request"].user.staff.clinic).get_available_slots(date),
            ]
        ):
            raise serializers.ValidationError({"visit": _("invalid or missing visit data")})

        return data

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

    def validate(self, attrs):
        data = super().validate(attrs)
        if any(
            [
                data["visit"].patient.clinic != self.context["request"].user.staff.clinic,
                data["supply"].clinic != self.context["request"].user.staff.clinic,
                data["quantity"] > data["supply"].remains,
            ]
        ):
            raise serializers.ValidationError({"visit": _("invalid visit data")})
        return data


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

    def validate(self, attrs):
        data = super().validate(attrs)
        if any(
            [
                data["visit"].patient.clinic != self.context["request"].user.staff.clinic,
                data["service"].clinic != self.context["request"].user.staff.clinic,
                not data["service"].active,
            ]
        ):
            raise serializers.ValidationError({"visit": _("invalid visit data")})
        return data


class ChargeServiceDetailSerializer(serializers.ModelSerializer):
    service = ServiceDetailSerializer(read_only=True)
    charge = serializers.FloatField(read_only=True)

    class Meta:
        model = ChargeService
        fields = "__all__"


class AvailableSlotListSerializer(serializers.Serializer):
    slots = serializers.ListField(child=serializers.TimeField())
