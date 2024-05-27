from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.system_management.admin import ClinicAdmin, TimeSlotInline
from clinic.system_management.factories import ClinicFactory
from clinic.system_management.models import Clinic
from clinic.visits.factories import TimeSlotFactory
from clinic.visits.models import TimeSlot


class ReportReviewMediaInlineTest(TestCase):
    def setUp(self):
        self.inline_admin = TimeSlotInline(TimeSlot, AdminSite())
        self.obj = TimeSlotFactory.create()
        self.request = None

    def test_has_add_permission(self):
        # Ensure that add permission is disabled
        self.assertFalse(self.inline_admin.has_add_permission(self.request, self.obj))

    def test_has_change_permission(self):
        # Ensure that add permission is disabled
        self.assertFalse(self.inline_admin.has_change_permission(self.request, self.obj))


class ClinicAdminTest(TestCase):
    def setUp(self):
        self.admin = ClinicAdmin(Clinic, AdminSite())
        self.obj = ClinicFactory.create()
        self.request = None

    def test_has_add_permission(self):
        # Ensure that add permission is disabled
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))

    def test_has_change_permission(self):
        # Ensure that add permission is disabled
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))
