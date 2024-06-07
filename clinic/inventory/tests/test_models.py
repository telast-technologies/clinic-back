from django.test import TestCase

from clinic.inventory.factories import SupplyFactory
from clinic.inventory.models import Supply
from clinic.invoices.factories import ChargeItemFactory


class SupplyModelTest(TestCase):
    def setUp(self):
        self.supply = SupplyFactory.create()

    def test_create_supply(self):
        self.assertIsInstance(self.supply, Supply)
        self.assertIsInstance(self.supply.__str__(), str)

    def test_display_label(self):
        self.assertEqual(self.supply.label, f"{self.supply.item} ({self.supply.unit_sales_price})")

    def test_display_remains_if_no_charges(self):
        self.assertEqual(self.supply.remains, self.supply.quantity)

    def test_display_remains_if_charges(self):
        ChargeItemFactory.create(quantity=10, supply=self.supply)
        self.assertEqual(self.supply.remains, self.supply.quantity - 10)

    def test_display_remains_if_charges_equal_supplies(self):
        ChargeItemFactory.create(quantity=self.supply.quantity, supply=self.supply)
        self.assertEqual(self.supply.remains, 0.0)
