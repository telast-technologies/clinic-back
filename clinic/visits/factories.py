from datetime import datetime

from factory import SubFactory
from factory.django import DjangoModelFactory


class TimeSlotFactory(DjangoModelFactory):
    class Meta:
        model = "visits.TimeSlot"

    clinic = SubFactory("clinic.system_management.factories.ClinicFactory")
    start_time = datetime.now().time()
    end_time = datetime.now().time()
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
