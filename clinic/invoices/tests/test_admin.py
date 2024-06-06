from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from clinic.invoices.admin import InvoiceAdmin
from clinic.invoices.factories import InvoiceFactory
from clinic.invoices.models import Invoice


class VisitAdminTest(TestCase):
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
