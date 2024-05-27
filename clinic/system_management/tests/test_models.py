from django.test import TestCase

from clinic.system_management.factories import ClinicFactory, ExposedPermissionFactory, PackageFactory
from clinic.system_management.models import Clinic, ExposedPermission, Package


class PackageModelTest(TestCase):
    def setUp(self):
        self.package = PackageFactory.create()

    def test_create_package(self):
        self.assertIsInstance(self.package, Package)
        self.assertIsInstance(self.package.__str__(), str)


class ExposedPermissionModelTest(TestCase):
    def setUp(self):
        self.exposed_permission = ExposedPermissionFactory.create()

    def test_create_exposed_permission(self):
        self.assertIsInstance(self.exposed_permission, ExposedPermission)
        self.assertIsInstance(self.exposed_permission.__str__(), str)


class ClinicModelTest(TestCase):
    def setUp(self):
        self.clinic = ClinicFactory.create()
        self.slot = self.clinic.time_slots.create(
            clinic=self.clinic,
            days=["monday"],
            start_time="10:00:00",
            end_time="12:00:00",
        )

    def test_create_clinic(self):
        self.assertIsInstance(self.clinic, Clinic)
        self.assertIsInstance(self.clinic.__str__(), str)

    def test_display_days(self):
        self.assertEqual(self.clinic.days, {"monday"})

    def test_get_slots(self):
        self.assertEqual(list(self.clinic.time_slots.all()), [self.slot])

    def test_display_slots(self):
        self.assertEqual(self.clinic.slots, {"monday": {10, 11, 12}})
