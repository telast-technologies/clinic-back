from django.test import TestCase

from clinic.patients.factories import PatientFactory, PatientReportFactory
from clinic.patients.models import Patient, PatientReport


class PatientModelTest(TestCase):
    def setUp(self):
        self.patient = PatientFactory.create()

    def test_create_patient(self):
        self.assertIsInstance(self.patient, Patient)
        self.assertIsInstance(self.patient.__str__(), str)

    def test_display_fullname(self):
        self.assertEqual(self.patient.get_full_name(), f"{self.patient.first_name} {self.patient.last_name}")


class PatientReportModelTest(TestCase):
    def setUp(self):
        self.report = PatientReportFactory.create()

    def test_create_join_request(self):
        self.assertIsInstance(self.report, PatientReport)
        self.assertIsInstance(self.report.__str__(), str)
