from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from clinic.staff.api.v1.serializers import StaffDetailSerializer, StaffListSerializer
from clinic.staff.factories import StaffFactory
from clinic.system_management.factories import ExposedPermissionFactory


class StaffViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff = StaffFactory.create()
        self.client.force_authenticate(user=self.staff.user)

    def test_retrieve_staff_list(self):
        # Test retrieving staff list
        staff = StaffFactory.create(clinic=self.staff.clinic)

        url = reverse("api:v1:staff:staff-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], StaffListSerializer([staff], many=True).data)

    def test_self_invalid_retrieve_staff_detail(self):
        # Test retrieving staff detail
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": self.staff.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_retrieve_staff_detail(self):
        # Test retrieving staff detail
        staff = StaffFactory.create(clinic=self.staff.clinic)
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": staff.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, StaffDetailSerializer(staff).data)

    def test_create_staff_invalid_missing_data(self):
        # Test creating staff with invalid data
        url = reverse("api:v1:staff:staff-list")
        invalid_data = {"user": {"username": "newuser"}}
        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_staff_invalid_mismatch_passowrd(self):
        # Test creating staff with invalid data
        url = reverse("api:v1:staff:staff-list")
        data = {
            "user": {
                "first_name": "new",
                "last_name": "user",
                "username": "newuser",
                "email": "newuser@example.com",
                "phone": "+201003908123",
                "password": "newuserpassword",
                "password_confirm": "notnewuserpassword",
            },
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_staff_missing_instance(self):
        # Test updating non-existing staff instance
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": 9999})  # Non-existing staff pk
        data = {"user": {"username": "updateduser", "email": "updateduser@example.com"}}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_staff_missing_instance(self):
        # Test deleting non-existing staff instance
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": 9999})  # Non-existing staff pk
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_self_update_staff_invalid_data(self):
        # Test updating staff with valid data
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": self.staff.pk})
        data = {
            "user": {
                "is_active": False,
            }
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_other_update_staff_invalid_data(self):
        # Test updating staff with valid data
        staff = StaffFactory.create()
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": staff.pk})
        data = {
            "user": {
                "is_active": False,
            }
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_staff_valid_data(self):
        # Test creating staff with valid data
        url = reverse("api:v1:staff:staff-list")
        data = {
            "user": {
                "first_name": "new",
                "last_name": "user",
                "username": "newuser",
                "email": "newuser@example.com",
                "phone": "+201003908123",
                "password": "newuserpassword",
                "password_confirm": "newuserpassword",
            },
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_staff_valid_data(self):
        # Test updating staff with valid data
        staff = StaffFactory.create(clinic=self.staff.clinic)

        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": staff.pk})
        data = {
            "user": {
                "is_active": False,
            }
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # refresh the user from the database
        staff.user.refresh_from_db()
        # Check if user is inactive
        self.assertFalse(staff.user.is_active)

    def test_update_staff_permissions(self):
        # Test updating staff with valid data
        staff = StaffFactory.create(clinic=self.staff.clinic)
        permissions = [ExposedPermissionFactory.create().pk]
        url = reverse("api:v1:staff:staff-detail", kwargs={"pk": staff.pk})
        data = {"permissions": permissions}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # refresh the user from the database
        staff.refresh_from_db()
        # Check if user is inactive
        self.assertEqual(staff.permissions.count(), 1)
        self.assertEqual(staff.permissions.first().pk, permissions[0])
