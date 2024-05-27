from django.test import RequestFactory, TestCase
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from clinic.users.api.v1.validators import PasswordValidator


class PasswordValidatorTest(TestCase):
    class TestSerializer(serializers.Serializer):
        password = serializers.CharField(required=False)
        password_confirm = serializers.CharField(required=False)

    def setUp(self):
        self.validator = PasswordValidator()
        self.request_factory = RequestFactory()

    def test_post_missing_passwords(self):
        request = self.request_factory.post("/")
        serializer = PasswordValidatorTest.TestSerializer(data={}, context={"request": request})

        with self.assertRaises(ValidationError) as context:
            self.validator(serializer.initial_data, serializer)

        self.assertIn("password", context.exception.detail)
        self.assertIn("invalid or missing password", context.exception.detail["password"])

    def test_post_passwords_mismatch(self):
        request = self.request_factory.post("/")
        data = {"password": "password123", "password_confirm": "password456"}
        serializer = PasswordValidatorTest.TestSerializer(data=data, context={"request": request})

        with self.assertRaises(ValidationError) as context:
            self.validator(serializer.initial_data, serializer)

        self.assertIn("password", context.exception.detail)
        self.assertIn("invalid or missing password", context.exception.detail["password"])

    def test_patch_missing_password_confirm(self):
        request = self.request_factory.patch("/")
        data = {"password": "password123"}
        serializer = PasswordValidatorTest.TestSerializer(data=data, context={"request": request})

        with self.assertRaises(ValidationError) as context:
            self.validator(serializer.initial_data, serializer)
        self.assertIn("password", context.exception.detail)
        self.assertIn("invalid or missing password", context.exception.detail["password"])

    def test_patch_missing_password(self):
        request = self.request_factory.patch("/")
        data = {"password_confirm": "password123"}
        serializer = PasswordValidatorTest.TestSerializer(data=data, context={"request": request})

        with self.assertRaises(ValidationError) as context:
            self.validator(serializer.initial_data, serializer)

        self.assertIn("password", context.exception.detail)
        self.assertIn("invalid or missing password", context.exception.detail["password"])

    def test_patch_passwords_mismatch(self):
        request = self.request_factory.patch("/")
        data = {"password": "password123", "password_confirm": "password456"}
        serializer = PasswordValidatorTest.TestSerializer(data=data, context={"request": request})

        with self.assertRaises(ValidationError) as context:
            self.validator(serializer.initial_data, serializer)

        self.assertIn("password", context.exception.detail)
        self.assertIn("invalid or missing password", context.exception.detail["password"])

    def test_post_valid_passwords(self):
        request = self.request_factory.post("/")
        data = {"password": "password123", "password_confirm": "password123"}
        serializer = PasswordValidatorTest.TestSerializer(data=data, context={"request": request})

        try:
            self.validator(serializer.initial_data, serializer)
        except ValidationError:
            self.fail("PasswordValidator raised ValidationError unexpectedly!")

    def test_patch_valid_passwords(self):
        request = self.request_factory.patch("/")
        data = {"password": "password123", "password_confirm": "password123"}
        serializer = PasswordValidatorTest.TestSerializer(data=data, context={"request": request})

        try:
            self.validator(serializer.initial_data, serializer)
        except ValidationError:
            self.fail("PasswordValidator raised ValidationError unexpectedly!")
