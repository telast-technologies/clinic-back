from django.test import TestCase

from clinic.inventory.choices import SupplyType
from clinic.inventory.factories import SupplyFactory
from clinic.inventory.models import Supply
from clinic.invoices.factories import ChargeItemFactory


class SupplyModelTest(TestCase):
    def setUp(self):
        self.obj = SupplyFactory.create()

    def test_create_instance(self):
        self.assertIsInstance(self.obj, Supply)
        self.assertIsInstance(self.obj.__str__(), str)

    def test_display_label(self):
        self.assertEqual(self.obj.label, f"{self.obj.item} ({self.obj.lot})")

    def test_display_remains_if_no_charges(self):
        self.assertEqual(self.obj.remains, self.obj.quantity)

    def test_display_remains_if_charges(self):
        ChargeItemFactory.create(quantity=10, supply=self.obj)
        self.assertEqual(self.obj.remains, self.obj.quantity - 10)

    def test_display_remains_if_charges_equal_supplies(self):
        ChargeItemFactory.create(quantity=self.obj.quantity, supply=self.obj)
        self.assertEqual(self.obj.remains, 0.0)

    def test_display_unit_sales_price(self):
        price = self.obj.unit_cost + (self.obj.unit_cost * (self.obj.profit_share / 100))
        expected = price if self.obj.supply_type == SupplyType.SUPPLEMENT else self.obj.unit_cost

        self.assertEqual(self.obj.unit_sales_price, expected)
