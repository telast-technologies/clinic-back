from factory import Faker, SubFactory
from factory.django import DjangoModelFactory


class PackageFactory(DjangoModelFactory):
    name = Faker("company")
    description = Faker("sentence")
    price = Faker("pyint")

    class Meta:
        model = "system_management.Package"


class ClinicFactory(DjangoModelFactory):
    package = SubFactory("clinic.system_management.factories.PackageFactory")
    name = Faker("company")
    address = Faker("address")
    phone = Faker("phone_number")
    email = Faker("email")
    website = Faker("url")

    class Meta:
        model = "system_management.Clinic"
