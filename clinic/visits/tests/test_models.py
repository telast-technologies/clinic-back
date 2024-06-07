from django.test import TestCase

from clinic.visits.factories import TimeSlotFactory, VisitFactory
from clinic.visits.models import TimeSlot, Visit


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
