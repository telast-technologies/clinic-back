from django.test import TestCase

from clinic.visits.factories import ChargeItemFactory, ChargeServiceFactory, TimeSlotFactory, VisitFactory
from clinic.visits.models import ChargeItem, ChargeService, TimeSlot, Visit


class TimeSlotModelTest(TestCase):
    def setUp(self):
        self.slot = TimeSlotFactory.create()

    def test_create_time_slot(self):
        assert isinstance(self.slot, TimeSlot)
        assert isinstance(self.slot.__str__(), str)


class VisitModelTest(TestCase):
    def setUp(self):
        self.visit = VisitFactory.create()

    def test_create_visit(self):
        assert isinstance(self.visit, Visit)
        assert isinstance(self.visit.__str__(), str)


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
