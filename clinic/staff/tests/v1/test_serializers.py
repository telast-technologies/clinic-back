from django.test import RequestFactory, TestCase

from clinic.staff.api.v1.serializers import StaffModifySerializer
from clinic.staff.factories import StaffFactory
from clinic.staff.models import Staff
from clinic.system_management.factories import ClinicFactory


class StaffModifySerializerTest(TestCase):
    def setUp(self):
        # Create a clinic for testing
        self.clinic = ClinicFactory.create(name="Test Clinic")
        self.staff = StaffFactory.create(clinic=self.clinic, is_client_admin=True)
        self.request = RequestFactory().get("/")
        self.request.user = self.staff.user

        # User data for testing
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "phone": "+201003908123",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
        }

        # Staff data for testing
        self.staff_data = {"user": self.user_data, "is_client_admin": True, "clinic": self.staff.clinic}

    def test_create_staff(self):
        serializer = StaffModifySerializer(data=self.staff_data, context={"request": self.request})
        staff = serializer.create(self.staff_data)
        self.assertIsInstance(staff, Staff)
        self.assertEqual(staff.user.username, self.user_data["username"])
        self.assertEqual(staff.user.email, self.user_data["email"])
        self.assertEqual(staff.clinic, self.staff.clinic)

    def test_update_staff(self):
        # Update data
        updated_user_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
        }

        updated_staff_data = {"user": updated_user_data}

        serializer = StaffModifySerializer(instance=self.staff, data=updated_staff_data, partial=True)
        updated_staff = serializer.update(self.staff, updated_staff_data)

        self.assertEqual(updated_staff.user.username, updated_user_data["username"])
        self.assertEqual(updated_staff.user.email, updated_user_data["email"])
