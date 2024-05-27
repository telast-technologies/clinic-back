from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.healthcare.admin import ServiceAdmin
from clinic.healthcare.factories import ServiceFactory
from clinic.healthcare.models import Service


class ServiceAdminTest(TestCase):
    def setUp(self):
        self.admin = ServiceAdmin(Service, AdminSite())
        self.obj = ServiceFactory.create()
        self.request = None

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))
