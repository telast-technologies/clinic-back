import factory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "patients.Patient"

    clinic = factory.SubFactory("clinic.system_management.factories.ClinicFactory")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    birthdate = factory.Faker("date")
    address = factory.Faker("address")


class PatientReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "patients.PatientReport"

    patient = factory.SubFactory("clinic.patients.factories.PatientFactory")
    document = factory.django.FileField()