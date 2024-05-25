from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.system_management.services.clinic_service import ClinicService
from clinic.visits.choices import VisitType


class VisitValidator:
    requires_context = True

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        clinic = serializer.context["request"].user.staff.clinic

        visit_type = attrs.get("visit_type", getattr(serializer.instance, "visit_type", None))
        patient = attrs.get("patient", getattr(serializer.instance, "patient", None))

        date = attrs.get("date", getattr(serializer.instance, "date", None))
        time = attrs.get("time", getattr(serializer.instance, "time", None))

        if patient and not patient.clinic == clinic:
            # Check if the patient and visit type are correct during updates
            raise serializers.ValidationError({"patient": _("Patient does not belong to the same clinic.")})

        if visit_type == VisitType.SCHEDULED:
            available_slots = ClinicService(clinic).get_available_slots(date)
            if time and time not in available_slots:
                raise serializers.ValidationError({"time": _("Selected time slot is not available.")})


class ChargeItemValidator:
    requires_context = True

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        if any(
            [
                attrs["visit"].patient.clinic != serializer.context["request"].user.staff.clinic,
                attrs["supply"].clinic != serializer.context["request"].user.staff.clinic,
                attrs["quantity"] > attrs["supply"].remains,
            ]
        ):
            raise serializers.ValidationError({"visit": _("Invalid visit data")})


class ChargeServiceValidator:
    requires_context = True

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        if any(
            [
                attrs["visit"].patient.clinic != serializer.context["request"].user.staff.clinic,
                attrs["service"].clinic != serializer.context["request"].user.staff.clinic,
                not attrs["service"].active,
            ]
        ):
            raise serializers.ValidationError({"visit": _("Invalid visit data")})
