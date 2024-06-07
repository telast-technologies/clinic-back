from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.invoices.admin import ChargeItemInline, ChargeServiceInline, InvoiceAdmin
from clinic.invoices.factories import ChargeItemFactory, ChargeServiceFactory, InvoiceFactory
from clinic.invoices.models import ChargeItem, ChargeService, Invoice


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


class InvoiceAdminTest(TestCase):
    def setUp(self):
        self.admin = InvoiceAdmin(Invoice, AdminSite())
        self.obj = InvoiceFactory.create()
        self.request = None

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request, self.obj))

    def test_has_change_permission(self):
        self.assertFalse(self.admin.has_change_permission(self.request, self.obj))

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request, self.obj))

    def test_display_balance(self):
        self.assertEqual(self.admin.balance(self.obj), self.obj.balance)

    def test_display_total(self):
        self.assertEqual(self.admin.total(self.obj), self.obj.total)
