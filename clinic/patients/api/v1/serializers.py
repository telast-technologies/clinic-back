from rest_framework import serializers

from clinic.patients.api.v1.validators import PatientReportValidator
from clinic.patients.models import Patient, PatientReport
from clinic.users.api.defaults import CurrentClinicDefault


class PatientSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Patient
        fields = "__all__"


class SelectPatientSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="get_full_name", read_only=True)
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
        validations = [PatientReportValidator()]
