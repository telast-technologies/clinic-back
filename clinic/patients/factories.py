import factory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "patients.Patient"

    clinic = factory.SubFactory("clinic.system_management.factories.ClinicFactory")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    nid = factory.Faker("ean8")
    channel = "facebook"


class PatientReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "patients.PatientReport"

    patient = factory.SubFactory("clinic.patients.factories.PatientFactory")
    document = factory.django.FileField()


class PatientPrescriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "patients.PatientPrescription"

    patient = factory.SubFactory("clinic.patients.factories.PatientFactory")
    examination = factory.Faker("sentence")
