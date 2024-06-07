from datetime import datetime

from factory import SubFactory
from factory.django import DjangoModelFactory

from clinic.visits.choices import VisitStatus, VisitType


class TimeSlotFactory(DjangoModelFactory):
    class Meta:
        model = "visits.TimeSlot"

    clinic = SubFactory("clinic.system_management.factories.ClinicFactory")
    start_time = datetime.now().time()
    end_time = datetime.now().time()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


class VisitFactory(DjangoModelFactory):
    class Meta:
        model = "visits.Visit"

    patient = SubFactory("clinic.patients.factories.PatientFactory")
    date = datetime.now().date()
    time = datetime.now().time()
    status = VisitStatus.BOOKED
    visit_type = VisitType.SCHEDULED
