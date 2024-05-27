from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.inventory.admin import SupplyAdmin
from clinic.inventory.factories import SupplyFactory
from clinic.inventory.models import Supply


class SupplyAdminTest(TestCase):
    def setUp(self):
        self.admin = SupplyAdmin(Supply, AdminSite())
        self.obj = SupplyFactory.create()
        self.request = None

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))

    def test_display_remains(self):
        self.assertEqual(self.admin.remains(self.obj), self.obj.remains)
