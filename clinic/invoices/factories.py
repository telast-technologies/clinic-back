
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = "invoices.Invoice"
        django_get_or_create = ("visit",)

    visit = SubFactory("clinic.visits.factories.VisitFactory")
    tax = Faker("pyint", min_value=0, max_value=100)
    discount = Faker("pyint", min_value=0, max_value=100)
    sub_total = Faker("pyint")