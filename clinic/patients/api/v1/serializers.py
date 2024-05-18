from rest_framework import serializers

from clinic.patients.models import Patient
from clinic.users.api.defaults import CurrentClinicDefault


class PatientSerializer(serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())

    class Meta:
        model = Patient
        fields = "__all__"
