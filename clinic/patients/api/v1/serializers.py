from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from clinic.patients.api.validators import PatientReportValidator
from clinic.patients.models import Patient, PatientPrescription, PatientReport
from clinic.users.api.defaults import CurrentClinicDefault


class PatientSerializer(CountryFieldMixin, serializers.ModelSerializer):
    clinic = serializers.HiddenField(default=CurrentClinicDefault())
    age = serializers.IntegerField(read_only=True)
    nid = serializers.CharField(
        required=False,
        max_length=14,
        help_text=_("National ID must be exactly 14 digits long."),
        validators=[
            RegexValidator(
                regex=r"^\d{14}$",  # Matches exactly 14 digits
                message=_("National ID must be exactly 14 digits long."),
                code="invalid_nid_length",
            ),
        ],
    )
    passport = serializers.CharField(
        required=False,
        max_length=10,
        help_text=_("Passport ID must be exactly 10 chars long."),
        validators=[
            RegexValidator(
                regex=r"^.{10}$",  # Matches exactly 10 characters
                message=_("National ID must be exactly 10 digits long."),
                code="invalid_nid_length",
            ),
        ],
    )

    class Meta:
        model = Patient
        fields = "__all__"


class SelectPatientSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source="get_full_name", read_only=True)
    value = serializers.CharField(source="uid", read_only=True)

    class Meta:
        model = Patient
        fields = ("label", "value")


class PatientReportSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(read_only=True)
    size = serializers.CharField(read_only=True)

    class Meta:
        model = PatientReport
        fields = "__all__"
        validations = [PatientReportValidator()]


class PatientPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPrescription
        fields = "__all__"
        validations = [PatientReportValidator()]
