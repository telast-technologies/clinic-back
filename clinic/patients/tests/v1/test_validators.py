from django.test import RequestFactory, TestCase
from rest_framework import serializers

from clinic.patients.api.v1.serializers import PatientReportSerializer
from clinic.patients.api.v1.validators import PatientReportValidator
from clinic.patients.factories import PatientFactory
from clinic.staff.factories import StaffFactory
from clinic.system_management.factories import ClinicFactory


class PatientReportValidatorTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.other_clinic = ClinicFactory.create(name="Other Clinic")

        self.staff = StaffFactory.create(clinic=self.clinic)
        self.patient = PatientFactory.create(clinic=self.clinic)
        self.other_patient = PatientFactory.create(clinic=self.other_clinic)

        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        self.validator = PatientReportValidator()

    def test_invalid_patient__report_clinic(self):
        serializer = PatientReportSerializer(context={"request": self.request})
        attrs = {"patient": self.other_patient}

        with self.assertRaises(serializers.ValidationError) as context:
            self.validator(attrs, serializer)
        self.assertIn("patient", context.exception.detail)
        self.assertIn("Invalid patient", context.exception.detail["patient"])

    def test_valid_patient__report_clinic(self):
        serializer = PatientReportSerializer(context={"request": self.request})
        attrs = {"patient": self.patient}

        try:
            self.validator(attrs, serializer)
        except serializers.ValidationError:
            self.fail("PatientReportValidator raised ValidationError unexpectedly!")
