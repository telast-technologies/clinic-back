from django.test import TestCase

from clinic.invoices.factories import ChargeItemFactory, ChargeServiceFactory, InvoiceFactory
from clinic.invoices.models import ChargeItem, ChargeService, Invoice


class InvoiceModelTest(TestCase):
    def setUp(self):
        self.invoice = InvoiceFactory.create(sub_total=100, tax=10, discount=5)

    def test_create_invoice(self):
        assert isinstance(self.invoice, Invoice)
        assert isinstance(self.invoice.__str__(), str)

    def test_display_charges(self):
        item = ChargeItemFactory.create(invoice=self.invoice)
        service = ChargeServiceFactory.create(invoice=self.invoice)

        self.assertEqual(self.invoice.charges, item.charge + service.charge)

    def test_display_tax_amount(self):
        self.assertEqual(self.invoice.tax_amount, (self.invoice.tax / 100) * self.invoice.charges)

    def test_display_discount_amount(self):
        self.assertEqual(self.invoice.discount_amount, (self.invoice.discount / 100) * self.invoice.charges)

    def test_display_total(self):
        self.assertEqual(
            self.invoice.total, self.invoice.charges + self.invoice.tax_amount - self.invoice.discount_amount
        )

    def test_display_balance(self):
        self.assertEqual(self.invoice.balance, self.invoice.sub_total - self.invoice.total)

    def test_display_label(self):
        self.assertEqual(
            self.invoice.label,
            f"invoice#{self.invoice.uid.split('-')[-1]} | {self.invoice.visit.patient.get_full_name()}",
        )


class ChargeItemModelTest(TestCase):
    def setUp(self):
        self.charge_item = ChargeItemFactory.create()

    def test_create_charge_item(self):
        assert isinstance(self.charge_item, ChargeItem)
        assert isinstance(self.charge_item.__str__(), str)

    def test_display_charge(self):
        self.assertEqual(self.charge_item.charge, self.charge_item.quantity * self.charge_item.supply.unit_sales_price)


class ChargeServiceModelTest(TestCase):
    def setUp(self):
        self.charge_service = ChargeServiceFactory.create()

    def test_create_charge_service(self):
        assert isinstance(self.charge_service, ChargeService)
        assert isinstance(self.charge_service.__str__(), str)

    def test_display_charge(self):
        self.assertEqual(self.charge_service.charge, self.charge_service.service.charge)
