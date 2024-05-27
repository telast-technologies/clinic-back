from django.test import TestCase

from clinic.patients.factories import PatientFactory
from clinic.patients.filters import PatientFilter, SelectPatientFilter


class PatientFilterTest(TestCase):
    def setUp(self):
        self.patient1 = PatientFactory.create(
            first_name="John",
            last_name="Doe",
        )
        self.patient2 = PatientFactory.create(
            first_name="Jane",
            last_name="Smith",
        )

    def test_filter_fullname(self):
        filterset = PatientFilter(data={"fullname": "john"})

        self.assertTrue(filterset.is_valid())
        filtered_queryset = filterset.qs
        self.assertIn(self.patient1, filtered_queryset)
        self.assertNotIn(self.patient2, filtered_queryset)


class SelectPatientFilterTest(TestCase):
    def setUp(self):
        self.patient1 = PatientFactory.create(
            first_name="John",
            last_name="Doe",
        )
        self.patient2 = PatientFactory.create(
            first_name="Jane",
            last_name="Smith",
        )

    def test_filter_fullname(self):
        filterset = SelectPatientFilter(data={"fullname": "John"})

        self.assertTrue(filterset.is_valid())
        filtered_queryset = filterset.qs
        self.assertIn(self.patient1, filtered_queryset)
        self.assertNotIn(self.patient2, filtered_queryset)
