from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


class SupplyFactory(DjangoModelFactory):
    class Meta:
        model = "inventory.Supply"

    clinic = SubFactory("clinic.system_management.factories.ClinicFactory")
    invoice = Faker("pyint", min_value=0, max_value=100)
    item = FuzzyText()
    profit_share = Faker("pyfloat", min_value=0, max_value=100)
    unit_cost = Faker("pyfloat", min_value=0, max_value=100)
    quantity = Faker("pyfloat", min_value=0, max_value=100)
