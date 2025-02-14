from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from clinic.patients.factories import PatientFactory, PatientReportFactory
from clinic.staff.factories import StaffFactory


class PatientReportViewSetTest(TestCase):
    def setUp(self):
        # Create user, staff, clinic, and patient
        self.staff = StaffFactory.create()
        self.clinic = self.staff.clinic
        self.patient = PatientFactory.create(clinic=self.clinic)

        # Create a PatientReport for the clinic
        self.obj = PatientReportFactory.create(patient=self.patient)

        # Set up the API client and authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.staff.user)

    def test_list_patient_reports(self):
        url = reverse("api:v1:patients:patient_report-list")
        response = self.client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the created patient report
        self.assertEqual(len(response.data["results"]), 1)

    def test_delete_patient_report(self):
        url = reverse("api:v1:patients:patient_report-detail", args=[self.obj.pk])
        response = self.client.delete(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_patient_report_not_found(self):
        url = reverse("api:v1:patients:patient_report-detail", args=["99999"])
        response = self.client.delete(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
