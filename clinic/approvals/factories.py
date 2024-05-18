from factory import Faker, SubFactory
from factory.django import DjangoModelFactory


class JoinRequestFactory(DjangoModelFactory):
    package = SubFactory("clinic.system_management.factories.PackageFactory")
    clinic_name = Faker("company")
    administrator_first_name = Faker("first_name")
    administrator_last_name = Faker("last_name")
    administrator_email = Faker("email")
    administrator_phone = Faker("phone_number")

    class Meta:
        model = "approvals.JoinRequest"
