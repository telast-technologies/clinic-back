from django.urls import reverse
from django.utils import timezone
from clinic.staff.factories import StaffFactory
from clinic.users.factories import UserFactory
from rest_framework import status
from rest_framework.test import APITestCase

class VisitDashboardViewTest(APITestCase):
    def setUp(self):
        self.staff = StaffFactory.create(is_client_admin=True)

        self.client.force_authenticate(user=self.staff.user)


    def test_get_by_admin(self):
        url = reverse("api:v1:dashboard:visit", kwargs={"start_date": timezone.now(), "end_date": timezone.now()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_non_admin(self):
        self.client.force_authenticate(user=UserFactory.create())
          
        url = reverse("api:v1:dashboard:visit", kwargs={"start_date": timezone.now(), "end_date": timezone.now()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)