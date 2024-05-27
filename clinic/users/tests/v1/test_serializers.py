from django.test import RequestFactory, TestCase

from clinic.users.api.v1.serializers import UserModifySerializer
from clinic.users.factories import UserFactory


class UserModifySerializerTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().post("/")

    def test_create_user_with_valid_passwords(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone": "1234567890",
            "is_active": True,
            "password": "password123",
        }
        serializer = UserModifySerializer(data=data, context={"request": self.request})
        user = serializer.create(data)

        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.check_password("password123"))

    def test_update_user_with_valid_password(self):
        user = UserFactory.create(password="oldpassword")

        data = {
            "password": "newpassword123",
        }
        serializer = UserModifySerializer(instance=user, data=data, context={"request": self.request}, partial=True)

        updated_user = serializer.update(user, data)

        self.assertTrue(updated_user.check_password("newpassword123"))

    def test_update_user_with_mismatched_passwords(self):
        user = UserFactory.create(password="oldpassword")

        data = {
            "is_active": False,
        }
        serializer = UserModifySerializer(instance=user, data=data, context={"request": self.request}, partial=True)
        updated_user = serializer.update(user, data)

        self.assertEqual(updated_user.is_active, False)
        self.assertTrue(updated_user.check_password("oldpassword"))
