from django.test import TestCase

from clinic.invoices.factories import InvoiceFactory
from clinic.invoices.models import Invoice

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.invoice = InvoiceFactory.create(sub_total=100, tax=10, discount=5)

    def test_create_invoice(self):
        assert isinstance(self.invoice, Invoice)
        assert isinstance(self.invoice.__str__(), str)
    
    def test_display_tax_amount(self):
        self.assertEqual(self.invoice.tax_amount, (self.invoice.tax / 100) * self.invoice.sub_total)
    
    def test_display_discount_amount(self):
        self.assertEqual(self.invoice.discount_amount, (self.invoice.discount / 100) * self.invoice.sub_total)
    
    def test_display_total(self):
        self.assertEqual(self.invoice.total, self.invoice.sub_total + self.invoice.tax_amount - self.invoice.discount_amount)
    
    def test_display_balance(self):
        self.assertEqual(self.invoice.balance, self.invoice.total - self.invoice.visit.charges)
    
