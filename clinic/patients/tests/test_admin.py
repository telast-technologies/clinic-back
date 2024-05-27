from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.patients.admin import PatientAdmin, PatientReportInline
from clinic.patients.factories import PatientFactory, PatientReportFactory
from clinic.patients.models import Patient, PatientReport


class PatientReportInlineAdminTest(TestCase):
    def setUp(self):
        self.inline_admin = PatientReportInline(PatientReport, AdminSite())
        self.obj = PatientReportFactory.create()
        self.request = None

    def test_has_change_permission(self):
        self.assertFalse(self.inline_admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.inline_admin.has_add_permission(self.request, self.obj))


class PatientAdminTest(TestCase):
    def setUp(self):
        self.admin = PatientAdmin(Patient, AdminSite())
        self.obj = PatientFactory.create()
        self.request = None

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))
