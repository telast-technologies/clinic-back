from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PatientReportValidator:
    requires_context = True
    message = _("Invalid patient")

    def __call__(self, attrs: dict, serializer: serializers.ModelSerializer) -> None:
        if attrs.get("patient").clinic != serializer.context["request"].user.staff.clinic:
            raise serializers.ValidationError({"patient": self.message})
