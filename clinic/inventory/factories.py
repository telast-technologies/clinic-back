from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from clinic.inventory.choices import SupplyType


class SupplyFactory(DjangoModelFactory):
    class Meta:
        model = "inventory.Supply"

    clinic = SubFactory("clinic.system_management.factories.ClinicFactory")
    invoice = Faker("pyint", min_value=0, max_value=100)
    item = FuzzyText()
    unit_cost = Faker("pyfloat", min_value=0, max_value=100)
    quantity = 100
    expires_at = Faker("future_datetime")
    supply_type = SupplyType.SUPPLEMENT
