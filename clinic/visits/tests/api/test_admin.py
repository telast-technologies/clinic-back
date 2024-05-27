from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.visits.admin import ChargeItemInline, ChargeServiceInline, VisitAdmin
from clinic.visits.factories import ChargeItemFactory, ChargeServiceFactory, VisitFactory
from clinic.visits.models import ChargeItem, ChargeService, Visit


class ChargeItemInlineAdminTest(TestCase):
    def setUp(self):
        self.inline_admin = ChargeItemInline(ChargeItem, AdminSite())
        self.obj = ChargeItemFactory.create()
        self.request = None

    def test_has_change_permission(self):
        self.assertFalse(self.inline_admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.inline_admin.has_add_permission(self.request, self.obj))

    def test_display_charge(self):
        self.assertEqual(self.inline_admin.charge(self.obj), self.obj.charge)

    def test_display_remains(self):
        self.assertEqual(self.inline_admin.remains(self.obj), self.obj.supply.remains)


class ChargeServiceInlineAdminTest(TestCase):
    def setUp(self):
        self.inline_admin = ChargeServiceInline(ChargeService, AdminSite())
        self.obj = ChargeServiceFactory.create()
        self.request = None

    def test_has_change_permission(self):
        self.assertFalse(self.inline_admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.inline_admin.has_add_permission(self.request, self.obj))

    def test_display_charge(self):
        self.assertEqual(self.inline_admin.charge(self.obj), self.obj.charge)


class VisitAdminTest(TestCase):
    def setUp(self):
        self.admin = VisitAdmin(Visit, AdminSite())
        self.obj = VisitFactory.create()
        self.request = None

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))
