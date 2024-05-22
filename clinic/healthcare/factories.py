from factory import Faker, SubFactory
from factory.django import DjangoModelFactory


class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = "healthcare.Service"

    clinic = SubFactory("clinic.system_management.factories.ClinicFactory")
    name = Faker("name")
    charge = Faker("pyfloat", min_value=0.0, max_value=100.0)
    active = True
