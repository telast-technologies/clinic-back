from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clinic.patients.models import Patient, PatientReport
from clinic.users.api.defaults import CurrentClinicDefault


class PatientSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Patient
        fields = "__all__"


class SelectPatientSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="fullname", read_only=True)
    value = serializers.CharField(source="uid", read_only=True)

    class Meta:
        model = Patient
        fields = ["label", "value"]


class PatientReportSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="document.name", read_only=True)
    size = serializers.CharField(source="document.size", read_only=True)

    class Meta:
        model = PatientReport
        fields = "__all__"

        def validate(self, data):
            data = super(PatientReportSerializer, self).validate(data)

            patient = data.get("patient")
            if any([patient.clinic != self.context["request"].user.staff.clinic]):
                raise serializers.ValidationError({"patient": _("invalid patient")})

            return data
