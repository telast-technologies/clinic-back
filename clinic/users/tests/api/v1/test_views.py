from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from clinic.users.factories import UserFactory
from clinic.utils.notifications import send_inbox


class NotificationsInboxViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_inbox(self):
        send_inbox(self.user, recipient_list=[self.user.email], title="Test title", message="Test message")
        send_inbox(self.user, recipient_list=[UserFactory.create().email], title="Test title 2", message="Test message 2")

        url = reverse("api:v1:users:notification_inbox-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
