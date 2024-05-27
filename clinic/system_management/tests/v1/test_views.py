from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from clinic.staff.factories import StaffFactory


class ClinicProfileViewTest(TestCase):
    def setUp(self):
        # Set up user, staff, and clinic
        self.staff = StaffFactory.create(is_client_admin=True)

        # Set up the API client and authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.staff.user)

    def test_update_clinic_profile(self):
        data = {
            "capacity": 10,
        }
        url = reverse("api:v1:system_management:clinic-update-profile")
        # Simulate a GET request to the ClinicProfileView
        response = self.client.patch(url, data, format="json")
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the response data
        self.assertEqual(self.staff.clinic.capacity, 10)
