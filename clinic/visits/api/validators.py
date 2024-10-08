from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.system_management.services.clinic_service import ClinicService
from clinic.visits.choices import VisitType


class TimeSlotValidator:
    requires_context = True

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        start_time = attrs.get("start_time", getattr(serializer.instance, "start_time", None))
        end_time = attrs.get("end_time", getattr(serializer.instance, "end_time", None))

        if not start_time or not end_time:
            raise serializers.ValidationError({"time_slot": _("Invalid missing time slot.")})

        if start_time and end_time and end_time < start_time:
            raise serializers.ValidationError({"time_slot": _("Invalid range of time slot.")})


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
