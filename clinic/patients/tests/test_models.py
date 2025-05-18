import humanize
from django.test import TestCase
from django.utils import timezone

from clinic.patients.factories import PatientFactory, PatientPrescriptionFactory, PatientReportFactory
from clinic.patients.models import Patient, PatientPrescription, PatientReport


class PatientModelTest(TestCase):
    def setUp(self):
        self.obj = PatientFactory.create(birthdate=timezone.now() - timezone.timedelta(days=365 * 30))

    def test_create_instance(self):
        self.assertIsInstance(self.obj, Patient)
        self.assertIsInstance(self.obj.__str__(), str)

    def test_display_fullname(self):
        self.assertEqual(self.obj.get_full_name(), f"{self.obj.first_name} {self.obj.last_name}")

    def test_display_age(self):
        self.assertEqual(self.obj.age, (timezone.now() - self.obj.birthdate).days // 365)


class PatientReportModelTest(TestCase):
    def setUp(self):
        self.obj = PatientReportFactory.create()

    def test_create_instance(self):
        self.assertIsInstance(self.obj, PatientReport)
        self.assertIsInstance(self.obj.__str__(), str)

    def test_display_filename(self):
        self.assertEqual(self.obj.filename, self.obj.document.name.split("/")[-1])

    def test_display_size(self):
        self.assertEqual(self.obj.size, humanize.naturalsize(self.obj.document.size))


class PatientPrescriptionModelTest(TestCase):
    def setUp(self):
        self.obj = PatientPrescriptionFactory.create()

    def test_create_instance(self):
        self.assertIsInstance(self.obj, PatientPrescription)
        self.assertIsInstance(self.obj.__str__(), str)
