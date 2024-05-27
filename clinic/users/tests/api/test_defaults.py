from django.test import RequestFactory, TestCase
from rest_framework import serializers

from clinic.staff.factories import StaffFactory
from clinic.users.api.defaults import CurrentClinicDefault
from clinic.users.factories import UserFactory


class CurrentClinicDefaultTest(TestCase):
    class TestSerializer(serializers.Serializer):
        clinic = CurrentClinicDefault()

    def setUp(self):
        # Create a user with staff attribute
        self.default = CurrentClinicDefault()

    def test_current_staff_clinic_default(self):
        # Create a request object with the user
        staff = StaffFactory.create()
        request = RequestFactory().get("/")
        request.user = staff.user
        # Pass the request object to the serializer context
        serializer = CurrentClinicDefaultTest.TestSerializer(context={"request": request})
        result = self.default(serializer)
        # Validate that the serializer returns the correct clinic for the user
        self.assertEqual(result, staff.clinic)

    def test_current_no_staff_clinic_default(self):
        # Create a request object with the user
        request = RequestFactory().get("/")
        request.user = UserFactory.create()

        # Pass the request object to the serializer context
        serializer = CurrentClinicDefaultTest.TestSerializer(context={"request": request})
        result = self.default(serializer)
        # Validate that the serializer returns the correct clinic for the user
        self.assertEqual(result, None)
