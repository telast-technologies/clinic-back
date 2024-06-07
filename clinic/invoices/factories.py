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


class ChargeItemFactory(DjangoModelFactory):
    class Meta:
        model = "invoices.ChargeItem"

    invoice = SubFactory("clinic.invoices.factories.InvoiceFactory")
    supply = SubFactory("clinic.inventory.factories.SupplyFactory")
    quantity = 1


class ChargeServiceFactory(DjangoModelFactory):
    class Meta:
        model = "invoices.ChargeService"

    invoice = SubFactory("clinic.invoices.factories.InvoiceFactory")
    service = SubFactory("clinic.healthcare.factories.ServiceFactory")
