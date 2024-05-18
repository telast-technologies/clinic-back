from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from clinic.system_management.models import ExposedPermission


class PackageFactory(DjangoModelFactory):
    name = "free_trial"
    description = Faker("sentence")
    price = Faker("pyint")

    class Meta:
        model = "system_management.Package"
        django_get_or_create = ("name",)


class ClinicFactory(DjangoModelFactory):
    package = SubFactory("clinic.system_management.factories.PackageFactory")
    name = Faker("company")
    address = Faker("address")
    phone = Faker("phone_number")
    email = Faker("email")
    website = Faker("url")

    class Meta:
        model = "system_management.Clinic"


class PermissionFactory(DjangoModelFactory):
    name = Faker("name")
    codename = Faker("name")
    content_type = LazyAttribute(lambda o: ContentType.objects.get_for_model(Permission))

    class Meta:
        model = Permission


class ExposedPermissionFactory(DjangoModelFactory):
    permission = SubFactory(PermissionFactory)

    class Meta:
        model = ExposedPermission
        django_get_or_create = ["permission"]
