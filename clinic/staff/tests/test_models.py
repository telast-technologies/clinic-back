from django.test import TestCase

from clinic.staff.factories import StaffFactory
from clinic.staff.models import Staff


class StaffModelTest(TestCase):
    def setUp(self):
        self.staff = StaffFactory.create()

    def test_create_staff(self):
        self.assertIsInstance(self.staff, Staff)
        self.assertIsInstance(self.staff.__str__(), str)
