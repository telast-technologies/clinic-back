from factory import SubFactory
from factory.django import DjangoModelFactory


class StaffFactory(DjangoModelFactory):
    class Meta:
        model = "staff.Staff"

    user = SubFactory("clinic.users.factories.UserFactory", password="0000")
    clinic = SubFactory("clinic.system_management.factories.ClinicFactory")
